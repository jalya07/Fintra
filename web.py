from datetime import date

from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

import database
import tools

app = FastAPI(title="Fintra")
templates = Jinja2Templates(directory="web/templates")
app.mount("/static", StaticFiles(directory="web/static"), name="static")

SESSION_COOKIE = "fintra_session"
SESSION_HOURS = 24

# Как показывать категории на сайте: эмодзи, название, цвет для графика
CATEGORY_INFO = {
    "food":          ("🍔", "Food",          "#0B1F44"),
    "groceries":     ("🛒", "Groceries",     "#C9A227"),
    "cafe":          ("☕", "Cafe",          "#D9922B"),
    "transport":     ("🚕", "Transport",     "#2A9D8F"),
    "education":     ("📚", "Education",     "#4D5E86"),
    "entertainment": ("🎬", "Entertainment", "#8B1E2D"),
    "clothes":       ("👕", "Clothes",       "#7687B2"),
    "health":        ("💊", "Health",        "#5A8F7B"),
    "communication": ("📱", "Communication", "#B08D57"),
    "other":         ("📦", "Other",         "#9A8F7A"),
}
SOURCE_ICONS = {"text": "💬", "photo": "📸", "voice": "🎙"}
PERIOD_OPTIONS = [
    ("today", "Today"),
    ("week", "This week"),
    ("month", "This month"),
    ("all", "All time"),
]

# Цвета статусов лимитов (из нашей палитры)
OK_COLOR, WARNING_COLOR, DANGER_COLOR = "#2A9D8F", "#D9922B", "#8B1E2D"


@app.on_event("startup")
def startup():
    database.init_db()


# ---------- 🔐 Вход и выход ----------

def current_user(request: Request):
    """Telegram ID вошедшего пользователя или None."""
    return database.get_session_user(request.cookies.get(SESSION_COOKIE))


@app.get("/welcome", response_class=HTMLResponse)
async def welcome(request: Request, error: int = 0):
    return templates.TemplateResponse(request, "welcome.html", {"error": error})


@app.get("/login")
async def login(token: str = ""):
    user_id = database.use_login_token(token) if token else None
    if user_id is None:
        return RedirectResponse("/welcome?error=1", status_code=303)

    session_token = database.create_session(user_id, hours=SESSION_HOURS)
    response = RedirectResponse("/", status_code=303)
    response.set_cookie(
        SESSION_COOKIE,
        session_token,
        httponly=True,                   # JavaScript не может прочитать cookie
        samesite="lax",                  # защита от запросов с чужих сайтов
        max_age=SESSION_HOURS * 3600,
        secure=False,                    # True, когда сайт будет на HTTPS
    )
    return response


@app.get("/logout")
async def logout(request: Request):
    database.delete_session(request.cookies.get(SESSION_COOKIE))
    response = RedirectResponse("/welcome", status_code=303)
    response.delete_cookie(SESSION_COOKIE)
    return response


def render_page(request: Request, template: str, active: str, **context):
    """Общая логика страниц: без входа отправляем на /welcome."""
    user_id = current_user(request)
    if user_id is None:
        return RedirectResponse("/welcome", status_code=303)
    return templates.TemplateResponse(
        request, template, {"active": active, "user_id": user_id, **context}
    )


# ---------- Данные для Overview ----------

def build_overview(user_id):
    """Собирает данные главной страницы из тех же функций, что использует бот."""
    today = date.today().isoformat()

    # «Сколько можно сегодня» и план
    allowance = tools.get_daily_allowance(user_id)
    if allowance.get("status") == "no_budget":
        allowance, plan = None, None
    else:
        budget = database.get_budget(user_id)
        obligations_total = sum(o["amount"] for o in budget["obligations"])
        free = budget["income"] - obligations_total
        savings = round(free * budget["savings_percent"] / 100, 2)
        plan = {"spendable": round(free - savings, 2), "savings": savings,
                "savings_percent": budget["savings_percent"]}

    # Траты за месяц и данные для графика-бублика
    month = tools.get_summary(user_id, "month")
    circumference = 238.8  # длина окружности бублика (2 * π * 38)
    categories, offset = [], 0.0
    for row in month["by_category"]:
        emoji, label, color = CATEGORY_INFO.get(row["category"], CATEGORY_INFO["other"])
        share = row["total"] / month["total"] if month["total"] else 0
        dash = round(share * circumference, 1)
        categories.append({"emoji": emoji, "label": label, "color": color,
                           "total": row["total"], "percent": round(share * 100),
                           "dash": dash, "offset": round(offset, 1)})
        offset += dash

    # Последние 5 трат
    recent = []
    for e in database.get_recent_expenses(user_id, limit=5):
        emoji, label, _ = CATEGORY_INFO.get(e["category"], CATEGORY_INFO["other"])
        recent.append({**e, "emoji": emoji, "label": label,
                       "source_icon": SOURCE_ICONS.get(e["source"], "💬")})

    # Лимиты: сколько потрачено и статус
    month_start = date.today().replace(day=1).isoformat()
    limits = []
    for lim in database.get_limits(user_id):
        if lim["scope"] == "category":
            spent = database.get_spent(user_id, month_start, today, category=lim["target"])
            emoji, label, _ = CATEGORY_INFO.get(lim["target"], CATEGORY_INFO["other"])
        else:
            spent = database.get_spent(user_id, month_start, today, card=lim["target"])
            emoji, label = "💳", lim["target"]
        percent = round(spent / lim["amount"] * 100)
        if percent > 100:
            status, color = "Over limit", DANGER_COLOR
        elif percent >= 80:
            status, color = "Close to limit", WARNING_COLOR
        else:
            status, color = "On track", OK_COLOR
        limits.append({"emoji": emoji, "label": label, "spent": spent,
                       "amount": lim["amount"], "percent": percent,
                       "status": status, "color": color})

    return {
        "allowance": allowance,
        "plan": plan,
        "spent_today": database.get_spent(user_id, today, today),
        "month": month,
        "month_count": database.count_expenses(user_id, month_start, today),
        "categories": categories,
        "recent": recent,
        "limits": limits,
        "category_options": [(k, v) for k, v in CATEGORY_INFO.items()],
    }


# ---------- Страницы ----------

@app.get("/", response_class=HTMLResponse)
async def overview(request: Request, added: int = 0):
    user_id = current_user(request)
    if user_id is None:
        return RedirectResponse("/welcome", status_code=303)
    return render_page(request, "overview.html", "overview",
                       added=added, **build_overview(user_id))


@app.post("/expenses/add")
async def add_expense_from_web(request: Request,
                               amount: float = Form(...),
                               category: str = Form(...),
                               description: str = Form("")):
    user_id = current_user(request)
    if user_id is None:
        return RedirectResponse("/welcome", status_code=303)

    # 🔐 Те же проверки, что и в боте: сумма > 0, категория из списка, номера карт не сохраняем
    result = tools.add_expense(user_id, amount, category, description=description or None)
    if result.get("error"):
        return render_page(request, "overview.html", "overview",
                           form_error=result.get("message", result["error"]),
                           **build_overview(user_id))
    return RedirectResponse("/?added=1", status_code=303)


@app.get("/expenses", response_class=HTMLResponse)
async def expenses(request: Request, period: str = "month",
                   category: str = "", source: str = "", deleted: int = 0):
    user_id = current_user(request)
    if user_id is None:
        return RedirectResponse("/welcome", status_code=303)

    # Даты периода считаем так же, как бот (через tools.get_summary)
    if period not in dict(PERIOD_OPTIONS):
        period = "month"
    summary = tools.get_summary(user_id, period)
    limit = 200

    rows = database.get_expenses(
        user_id, summary["from"], summary["to"],
        category=category or None, source=source or None, limit=limit,
    )
    expenses_list = []
    for e in rows:
        emoji, label, _ = CATEGORY_INFO.get(e["category"], CATEGORY_INFO["other"])
        expenses_list.append({**e, "emoji": emoji, "label": label,
                              "source_icon": SOURCE_ICONS.get(e["source"], "💬")})

    total = round(sum(e["amount"] for e in expenses_list), 2)
    count = len(expenses_list)
    stats = {"count": count, "total": total,
             "average": round(total / count, 2) if count else 0}

    return render_page(
        request, "expenses.html", "expenses",
        expenses=expenses_list, stats=stats, limit=limit, deleted=deleted,
        period=period, period_label=dict(PERIOD_OPTIONS)[period],
        period_options=PERIOD_OPTIONS,
        category=category, source=source,
        category_options=[(k, v) for k, v in CATEGORY_INFO.items()],
    )


@app.post("/expenses/{expense_id}/delete")
async def delete_expense_from_web(request: Request, expense_id: int):
    user_id = current_user(request)
    if user_id is None:
        return RedirectResponse("/welcome", status_code=303)
    database.delete_expense(user_id, expense_id)  # 🔐 удалит, только если трата твоя
    return RedirectResponse("/expenses?deleted=1", status_code=303)


@app.get("/plan", response_class=HTMLResponse)
async def plan(request: Request):
    return render_page(request, "plan.html", "plan")


@app.get("/chat", response_class=HTMLResponse)
async def chat(request: Request):
    return render_page(request, "chat.html", "chat")


@app.get("/security", response_class=HTMLResponse)
async def security_page(request: Request):
    return render_page(request, "security.html", "security")