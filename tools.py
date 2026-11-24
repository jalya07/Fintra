from datetime import datetime, timedelta
import database

# Фиксированный список категорий, чтобы графики были аккуратными
CATEGORIES = [
    "food", "groceries", "cafe", "transport", "education",
    "entertainment", "clothes", "health", "communication", "other",
]


# ---------- Python-функции (то, что реально выполняется) ----------

def add_expense(user_id, amount, category, description=None, date=None, currency="AZN"):
    if category not in CATEGORIES:
        category = "other"
    expense_id = database.add_expense(
        user_id=user_id,
        amount=amount,
        category=category,
        description=description,
        date=date,
        currency=currency,
    )
    return {"status": "saved", "id": expense_id, "amount": amount,
            "category": category, "currency": currency}


def get_summary(user_id, period="month", category=None):
    today = datetime.now().date()
    if period == "today":
        start = today
    elif period == "week":
        start = today - timedelta(days=today.weekday())  # понедельник этой недели
    elif period == "month":
        start = today.replace(day=1)
    else:  # "all"
        start = datetime(2000, 1, 1).date()

    rows = database.get_summary(
        user_id=user_id,
        start_date=start.isoformat(),
        end_date=today.isoformat(),
        category=category,
    )
    grand_total = round(sum(r["total"] for r in rows), 2)
    return {"period": period, "from": start.isoformat(), "to": today.isoformat(),
            "total": grand_total, "by_category": rows}


# ---------- Описания для модели (что она «видит») ----------

TOOL_DECLARATIONS = [
    {
        "name": "add_expense",
        "description": (
            "Save one expense of the user. Call it once per expense. "
            "If the user mentions several expenses, call it several times."
        ),
        "parameters_json_schema": {
            "type": "object",
            "properties": {
                "amount": {"type": "number", "description": "Amount spent, positive number"},
                "category": {"type": "string", "enum": CATEGORIES},
                "description": {"type": "string", "description": "Short description, e.g. 'coffee'"},
                "date": {"type": "string", "description": "Date in YYYY-MM-DD. Omit for today."},
                "currency": {"type": "string", "description": "AZN by default, or USD, EUR"},
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
]


# ---------- Запуск инструмента по имени ----------

TOOL_FUNCTIONS = {
    "add_expense": add_expense,
    "get_summary": get_summary,
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