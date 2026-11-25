import os
import calendar
from datetime import datetime, timedelta, date as Date

import matplotlib
matplotlib.use("Agg")  # рисовать в файл, без открытия окна (важно на Mac)
import matplotlib.pyplot as plt

import database
import security

# Папка для графиков (она в .gitignore)
CHARTS_DIR = "charts"

# Фиксированный список категорий, чтобы графики были аккуратными
CATEGORIES = [
    "food", "groceries", "cafe", "transport", "education",
    "entertainment", "clothes", "health", "communication", "other",
]

# С какого процента лимита предупреждать
LIMIT_WARNING_PERCENT = 80


# ---------- Вспомогательные функции ----------

def _payday_in_month(year, month, payday):
    """День зарплаты в конкретном месяце (если в месяце нет 31-го, берём последний день)."""
    last_day = calendar.monthrange(year, month)[1]
    return Date(year, month, min(payday, last_day))


def pay_period(payday):
    """Начало текущего периода (последняя зарплата) и дата следующей зарплаты."""
    today = Date.today()
    this_month = _payday_in_month(today.year, today.month, payday)

    if today >= this_month:
        start = this_month
        y, m = (today.year + 1, 1) if today.month == 12 else (today.year, today.month + 1)
        next_payday = _payday_in_month(y, m, payday)
    else:
        next_payday = this_month
        y, m = (today.year - 1, 12) if today.month == 1 else (today.year, today.month - 1)
        start = _payday_in_month(y, m, payday)

    return start, next_payday


def normalize_card(card):
    """Единый вид названия карты: ' birbank ' → 'BIRBANK'."""
    return card.strip().upper()


def check_limits(user_id, category, card=None):
    """После траты проверяет лимиты этого месяца. Возвращает предупреждения."""
    today = Date.today()
    start = today.replace(day=1).isoformat()
    warnings = []

    for lim in database.get_limits(user_id):
        if lim["scope"] == "category" and lim["target"] == category:
            spent = database.get_spent(user_id, start, today.isoformat(), category=category)
        elif lim["scope"] == "card" and card and lim["target"] == card:
            spent = database.get_spent(user_id, start, today.isoformat(), card=card)
        else:
            continue

        percent = round(spent / lim["amount"] * 100)
        if percent >= LIMIT_WARNING_PERCENT:
            warnings.append({
                "scope": lim["scope"], "target": lim["target"],
                "limit": lim["amount"], "spent": round(spent, 2), "percent": percent,
            })
    return warnings


# ---------- «Sayır»: учёт ----------

def add_expense(user_id, amount, category, description=None, date=None,
                currency="AZN", card=None):
    """Сохраняет одну трату и проверяет лимиты."""
    if amount <= 0:
        return {"error": "Amount must be positive"}
    if category not in CATEGORIES:
        category = "other"

    # 🔐 Номера карт никогда не сохраняем
    if card:
        if security.looks_like_card_number(card):
            return {"error": "card_number_rejected",
                    "message": "Never send card numbers. Use a card name like 'Birbank'."}
        card = normalize_card(card)
    if description and security.looks_like_card_number(description):
        description = "[hidden]"

    expense_id = database.add_expense(
        user_id=user_id, amount=amount, category=category,
        description=description, date=date, currency=currency, card=card,
    )
    return {
        "status": "saved", "id": expense_id, "amount": amount,
        "category": category, "currency": currency, "card": card,
        "limit_warnings": check_limits(user_id, category, card),
    }


def get_summary(user_id, period="month", category=None):
    """Итоги трат по категориям за период."""
    today = datetime.now().date()
    if period == "today":
        start = today
    elif period == "week":
        start = today - timedelta(days=today.weekday())  # понедельник этой недели
    elif period == "month":
        start = today.replace(day=1)
    else:  # "all"
        start = Date(2000, 1, 1)

    rows = database.get_summary(
        user_id=user_id, start_date=start.isoformat(),
        end_date=today.isoformat(), category=category,
    )
    grand_total = round(sum(r["total"] for r in rows), 2)
    return {"period": period, "from": start.isoformat(), "to": today.isoformat(),
            "total": grand_total, "by_category": rows}


def make_chart(user_id, period="month"):
    """Рисует график-бублик трат по категориям и сохраняет его в PNG."""
    summary = get_summary(user_id, period)
    rows = summary["by_category"]
    if not rows:
        return {"status": "empty", "message": "No expenses for this period"}

    labels = [r["category"] for r in rows]
    values = [r["total"] for r in rows]

    os.makedirs(CHARTS_DIR, exist_ok=True)
    path = os.path.join(CHARTS_DIR, f"{user_id}_{period}.png")

    fig, ax = plt.subplots(figsize=(6, 6))
    ax.pie(values, labels=labels, autopct="%1.0f%%", startangle=90,
           wedgeprops={"width": 0.45})
    ax.set_title(f"Fintra · {period} · {summary['total']} AZN")
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)

    return {"status": "created", "chart_path": path, "total": summary["total"]}


# ---------- «Planlayır»: планирование ----------

def plan_budget(user_id, income, payday, savings_percent, obligations=None):
    """План: доход − обязательные платежи − накопления = деньги на жизнь."""
    obligations = obligations or []
    payday = int(payday)

    # Проверка входных данных
    if income <= 0:
        return {"error": "Income must be positive"}
    if not 1 <= payday <= 31:
        return {"error": "Payday must be a day of month between 1 and 31"}
    if not 0 <= savings_percent <= 90:
        return {"error": "Savings percent must be between 0 and 90"}

    obligations_total = round(sum(o["amount"] for o in obligations), 2)
    if obligations_total > income:
        return {"error": "Obligations are bigger than income",
                "income": income, "obligations_total": obligations_total}

    free = income - obligations_total
    savings = round(free * savings_percent / 100, 2)
    spendable = round(free - savings, 2)

    database.save_budget(user_id, income, payday, savings_percent, obligations)
    allowance = get_daily_allowance(user_id)

    return {
        "status": "saved", "income": income,
        "obligations_total": obligations_total, "savings": savings,
        "spendable_per_month": spendable,
        "daily_allowance": allowance.get("daily_allowance"),
        "days_until_payday": allowance.get("days_until_payday"),
        "next_step": "You may suggest optional category limits. Set them only if the user agrees.",
    }


def get_daily_allowance(user_id):
    """Сколько можно потратить сегодня до следующей зарплаты."""
    budget = database.get_budget(user_id)
    if budget is None:
        return {"status": "no_budget",
                "message": "No plan yet. Ask the user for income, payday and obligations."}

    obligations_total = sum(o["amount"] for o in budget["obligations"])
    free = budget["income"] - obligations_total
    spendable = free - free * budget["savings_percent"] / 100

    start, next_payday = pay_period(budget["payday"])
    today = Date.today()
    spent = database.get_spent(user_id, start.isoformat(), today.isoformat())

    days_left = max((next_payday - today).days, 1)
    remaining = round(spendable - spent, 2)
    daily = round(max(remaining, 0) / days_left, 2)

    return {
        "daily_allowance": daily, "remaining_until_payday": remaining,
        "spent_since_payday": round(spent, 2), "days_until_payday": days_left,
        "next_payday": next_payday.isoformat(),
    }


def set_limit(user_id, scope, target, amount):
    """Лимит на категорию или карту (на календарный месяц)."""
    if scope not in ("category", "card"):
        return {"error": "Scope must be 'category' or 'card'"}
    if amount <= 0:
        return {"error": "Limit must be positive"}

    if scope == "category":
        if target not in CATEGORIES:
            return {"error": f"Unknown category. Use one of: {', '.join(CATEGORIES)}"}
    else:
        # 🔐 Лимит ставим на НАЗВАНИЕ карты, номер не принимаем
        if security.looks_like_card_number(target):
            return {"error": "card_number_rejected",
                    "message": "Never send card numbers. Use a card name like 'Birbank'."}
        target = normalize_card(target)

    database.set_limit(user_id, scope, target, amount)
    return {"status": "saved", "scope": scope, "target": target, "amount": amount}


# ---------- Описания для модели (что она «видит») ----------

TOOL_DECLARATIONS = [
    {
        "name": "add_expense",
        "description": (
            "Save one expense of the user. Call it once per expense. "
            "If the user mentions several expenses, call it several times. "
            "If the result has limit_warnings, warn the user."
        ),
        "parameters_json_schema": {
            "type": "object",
            "properties": {
                "amount": {"type": "number", "description": "Amount spent, positive number"},
                "category": {"type": "string", "enum": CATEGORIES},
                "description": {"type": "string", "description": "Short description, e.g. 'coffee'"},
                "date": {"type": "string", "description": "Date in YYYY-MM-DD. Omit for today."},
                "currency": {"type": "string", "description": "AZN by default, or USD, EUR"},
                "card": {"type": "string",
                         "description": "Optional card NAME the user paid with, e.g. 'Birbank'. Never a card number."},
            },
            "required": ["amount", "category"],
        },
    },
    {
        "name": "get_summary",
        "description": "Get the user's spending totals by category for a period.",
        "parameters_json_schema": {
            "type": "object",
            "properties": {
                "period": {"type": "string", "enum": ["today", "week", "month", "all"]},
                "category": {"type": "string", "enum": CATEGORIES,
                             "description": "Optional: only this category"},
            },
            "required": ["period"],
        },
    },
    {
        "name": "make_chart",
        "description": (
            "Create a donut chart of the user's spending by category for a period. "
            "The image is sent to the user automatically."
        ),
        "parameters_json_schema": {
            "type": "object",
            "properties": {
                "period": {"type": "string", "enum": ["today", "week", "month", "all"]},
            },
            "required": ["period"],
        },
    },
    {
        "name": "plan_budget",
        "description": (
            "Create or update the user's monthly budget plan. "
            "Call it ONLY after you know the income, the payday and the obligations, "
            "AND after the user has answered how much they want to save."
        ),
        "parameters_json_schema": {
            "type": "object",
            "properties": {
                "income": {"type": "number", "description": "Monthly income"},
                "payday": {"type": "integer", "description": "Day of month when income arrives, 1-31"},
                "savings_percent": {"type": "number",
                                    "description": "Percent of free money to save, chosen by the user (0 is allowed)"},
                "obligations": {
                    "type": "array",
                    "description": "Fixed monthly payments: rent, loans, utilities...",
                    "items": {
                        "type": "object",
                        "properties": {
                            "name": {"type": "string"},
                            "amount": {"type": "number"},
                        },
                        "required": ["name", "amount"],
                    },
                },
            },
            "required": ["income", "payday", "savings_percent"],
        },
    },
    {
        "name": "get_daily_allowance",
        "description": "How much the user can spend today until the next payday.",
        "parameters_json_schema": {"type": "object", "properties": {}},
    },
    {
        "name": "set_limit",
        "description": (
            "Set a monthly spending limit on a category or on a card. "
            "Call it only when the user explicitly agrees to the limit."
        ),
        "parameters_json_schema": {
            "type": "object",
            "properties": {
                "scope": {"type": "string", "enum": ["category", "card"]},
                "target": {"type": "string",
                           "description": "Category name from the list, or card NAME like 'Birbank'"},
                "amount": {"type": "number", "description": "Monthly limit"},
            },
            "required": ["scope", "target", "amount"],
        },
    },
]


# ---------- Запуск инструмента по имени ----------

TOOL_FUNCTIONS = {
    "add_expense": add_expense,
    "get_summary": get_summary,
    "make_chart": make_chart,
    "plan_budget": plan_budget,
    "get_daily_allowance": get_daily_allowance,
    "set_limit": set_limit,
}


def execute_tool(name, args, user_id):
    """Выполняет инструмент, который выбрала модель. user_id подставляет код, не модель."""
    func = TOOL_FUNCTIONS.get(name)
    if func is None:
        return {"error": f"Unknown tool: {name}"}
    try:
        return func(user_id=user_id, **args)
    except Exception as e:
        return {"error": str(e)}