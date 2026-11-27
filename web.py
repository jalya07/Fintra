from datetime import date

from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

import database
import tools
import glob
import os
import time
import secrets

from fastapi.responses import FileResponse, JSONResponse
from jinja2 import pass_context
from pydantic import BaseModel

import security
import i18n
from agent import run_agent
from tools import CHARTS_DIR
from dotenv import load_dotenv
load_dotenv()

# 🔐 Документация API (/docs) не нужна посторонним: выключаем
app = FastAPI(title="Fintra", docs_url=None, redoc_url=None, openapi_url=None)

# 🔐 Если сайт открыт по HTTPS, cookie отправляются только по защищённому соединению
COOKIE_SECURE = os.getenv("WEB_URL", "").startswith("https://")

templates = Jinja2Templates(directory="web/templates")
app.mount("/static", StaticFiles(directory="web/static"), name="static")


# ---------- 🌍 Язык сайта ----------

@pass_context
def jinja_t(context, text, **kwargs):
    """В шаблонах: {{ t("Add expense") }}. Язык берётся из контекста страницы."""
    return i18n.translate(context.get("lang", i18n.DEFAULT_LANG), text, **kwargs)


templates.env.globals["t"] = jinja_t


@app.middleware("http")
async def language_middleware(request: Request, call_next):
    """Определяем язык для каждого запроса и запоминаем выбор в cookie."""
    query_lang = request.query_params.get("lang")
    request.state.lang = i18n.pick_lang(
        query_lang,
        request.cookies.get(i18n.LANG_COOKIE),
        request.headers.get("accept-language"),
    )
    response = await call_next(request)
    if query_lang in i18n.LANGS:  # 🔐 сохраняем только az / ru / en
        response.set_cookie(i18n.LANG_COOKIE, query_lang, max_age=365 * 24 * 3600,
                            httponly=True, samesite="lax", secure=COOKIE_SECURE)
    return response

@app.middleware("http")
async def refresh_session(request: Request, call_next):
    """🔐 Скользящая сессия: пока человек пользуется сайтом, вход продлевается на 30 дней."""
    response = await call_next(request)
    token = request.cookies.get(SESSION_COOKIE)
    if not request.url.path.startswith("/static") and database.extend_session(token, SESSION_HOURS):
        response.set_cookie(SESSION_COOKIE, token, httponly=True, samesite="lax",
                            max_age=SESSION_HOURS * 3600, secure=COOKIE_SECURE)
    return response

def tr(request: Request, text, **kwargs):
    """Перевод в Python-коде (для ответов API)."""
    return i18n.translate(request.state.lang, text, **kwargs)


SESSION_COOKIE = "fintra_session"
SESSION_HOURS = 24 * 30

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
# Подсказки на странице чата (на языке сайта; пример мошеннического SMS всегда на азербайджанском)
SCAM_EXAMPLE = "Kartınız bloklanıb, SMS kodu göndərin: kapitalbank-az-secure.com"
CHAT_SUGGESTIONS = {
    "az": [("local_cafe", "qəhvə 3.5 manat"),
           ("today", "Bu gün nə qədər xərcləyə bilərəm?"),
           ("donut_large", "Bu ayın xərclərinin diaqramını göstər"),
           ("shield", SCAM_EXAMPLE)],
    "ru": [("local_cafe", "кофе 3.5 маната"),
           ("today", "Сколько я могу потратить сегодня?"),
           ("donut_large", "Покажи график моих расходов за месяц"),
           ("shield", SCAM_EXAMPLE)],
    "en": [("local_cafe", "coffee 3.5 manat"),
           ("today", "How much can I spend today?"),
           ("donut_large", "Show a chart of my spending this month"),
           ("shield", SCAM_EXAMPLE)],
}
# Сообщения на странице входа (?info=...)
WELCOME_INFO = {
    "logged_out": "You have been logged out.",
    "deleted": "All your data has been deleted.",
}

# 🔐 Запросы на подтверждение из веб-чата (хранятся только в памяти сервера)
PENDING = {}
CONFIRM_TTL_SECONDS = 300


class ChatRequest(BaseModel):
    message: str


class ConfirmRequest(BaseModel):
    token: str
    action: str

@app.on_event("startup")
def startup():
    database.init_db()


# ---------- 🔐 Вход и выход ----------

def current_user(request: Request):
    """Telegram ID вошедшего пользователя или None."""
    return database.get_session_user(request.cookies.get(SESSION_COOKIE))


@app.get("/welcome", response_class=HTMLResponse)
async def welcome(request: Request, error: int = 0, info: str = ""):
    return templates.TemplateResponse(request, "welcome.html", {
        "error": error, "info": WELCOME_INFO.get(info, ""), "lang": request.state.lang,
    })

@app.get("/sw.js", include_in_schema=False)
async def service_worker():
    """📱 Service worker должен лежать в корне сайта, чтобы работать на всех страницах."""
    return FileResponse("web/static/sw.js", media_type="application/javascript",
                        headers={"Cache-Control": "no-cache"})

@app.get("/privacy", response_class=HTMLResponse)
async def privacy(request: Request):
    """Политика конфиденциальности: открыта всем, вход не нужен."""
    return templates.TemplateResponse(request, "privacy.html", {"lang": request.state.lang})

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
        secure=COOKIE_SECURE,  # 🔐 только HTTPS, когда сайт публичный
    )
    return response


@app.get("/logout")
async def logout(request: Request):
    database.delete_session(request.cookies.get(SESSION_COOKIE))
    response = RedirectResponse("/welcome?info=logged_out", status_code=303)
    response.delete_cookie(SESSION_COOKIE)
    return response


def render_page(request: Request, template: str, active: str, **context):
    """Общая логика страниц: без входа отправляем на /welcome."""
    user_id = current_user(request)
    if user_id is None:
        return RedirectResponse("/welcome", status_code=303)
    return templates.TemplateResponse(
        request, template,
        {"active": active, "user_id": user_id, "lang": request.state.lang, **context}
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
                       "scope": lim["scope"], "target": lim["target"],
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


# ---------- Plan & Limits ----------

def build_plan_page(user_id):
    """Данные страницы Plan & Limits."""
    budget = database.get_budget(user_id)
    plan = None
    if budget:
        obligations_total = round(sum(o["amount"] for o in budget["obligations"]), 2)
        free = budget["income"] - obligations_total
        savings = round(free * budget["savings_percent"] / 100, 2)
        spendable = round(free - savings, 2)
        income = budget["income"]
        plan = {
            "income": income, "payday": budget["payday"],
            "savings_percent": budget["savings_percent"],
            "obligations": budget["obligations"], "obligations_total": obligations_total,
            "savings": savings, "spendable": spendable,
            # Доли для полосы распределения дохода (в процентах)
            "share_obligations": round(obligations_total / income * 100),
            "share_savings": round(savings / income * 100),
            "share_spendable": round(spendable / income * 100),
        }
    allowance = tools.get_daily_allowance(user_id) if budget else None
    return {
        "plan": plan,
        "allowance": allowance,
        "limits": build_overview(user_id)["limits"],
        "category_options": [(k, v) for k, v in CATEGORY_INFO.items()],
    }


@app.get("/plan", response_class=HTMLResponse)
async def plan(request: Request, message: str = "", error: str = ""):
    user_id = current_user(request)
    if user_id is None:
        return RedirectResponse("/welcome", status_code=303)
    return render_page(request, "plan.html", "plan",
                       message=message, error=error, **build_plan_page(user_id))


def plan_redirect(message="", error=""):
    """Возврат на страницу плана с сообщением (паттерн Post/Redirect/Get)."""
    from urllib.parse import urlencode
    query = urlencode({k: v for k, v in {"message": message, "error": error}.items() if v})
    return RedirectResponse(f"/plan?{query}", status_code=303)


@app.post("/plan/save")
async def save_plan(request: Request):
    user_id = current_user(request)
    if user_id is None:
        return RedirectResponse("/welcome", status_code=303)

    form = await request.form()
    try:
        income = float(form["income"])
        payday = int(form["payday"])
        savings_percent = float(form["savings_percent"])
    except (KeyError, ValueError):
        return plan_redirect(error="Please fill income, payday and savings with numbers")

    # Обязательные платежи: пары «название + сумма», пустые строки пропускаем
    obligations = []
    for name, amount in zip(form.getlist("ob_name"), form.getlist("ob_amount")):
        name = name.strip()
        if name and amount:
            obligations.append({"name": name[:40], "amount": float(amount)})

    # 🔐 Те же проверки, что у агента
    result = tools.plan_budget(user_id, income, payday, savings_percent, obligations)
    if result.get("error"):
        return plan_redirect(error=result["error"])
    return plan_redirect(message="Plan saved")


@app.post("/limits/add")
async def add_limit(request: Request,
                    scope: str = Form(...),
                    amount: float = Form(...),
                    category: str = Form(""),
                    card: str = Form("")):
    user_id = current_user(request)
    if user_id is None:
        return RedirectResponse("/welcome", status_code=303)

    target = category if scope == "category" else card.strip()
    result = tools.set_limit(user_id, scope, target, amount)  # 🔐 номер карты будет отклонён
    if result.get("error"):
        return plan_redirect(error=result.get("message", result["error"]))
    return plan_redirect(message="Limit saved")


@app.post("/limits/remove")
async def remove_limit(request: Request, scope: str = Form(...), target: str = Form(...)):
    user_id = current_user(request)
    if user_id is None:
        return RedirectResponse("/welcome", status_code=303)
    # Человек сам нажал кнопку и подтвердил в окне. Удаляем только свой лимит
    removed = database.remove_limit(user_id, scope, target)
    return plan_redirect(message="Limit removed") if removed else plan_redirect(error="Limit not found")

@app.get("/chat", response_class=HTMLResponse)
async def chat(request: Request):
    return render_page(request, "chat.html", "chat",
                       suggestions=CHAT_SUGGESTIONS[request.state.lang])

SECURITY_MESSAGES = {
    "logged_out": "You have been logged out on all devices.",
}
SECURITY_ERRORS = {
    "confirm": "Data was NOT deleted: type DELETE exactly to confirm.",
}


@app.get("/security", response_class=HTMLResponse)
async def security_page(request: Request, message: str = "", error: str = ""):
    user_id = current_user(request)
    if user_id is None:
        return RedirectResponse("/welcome", status_code=303)
    return render_page(
        request, "security.html", "security",
        data=database.get_data_stats(user_id),
        message=SECURITY_MESSAGES.get(message, ""),
        error=SECURITY_ERRORS.get(error, ""),
    )


@app.post("/security/logout-all")
async def security_logout_all(request: Request):
    user_id = current_user(request)
    if user_id is None:
        return RedirectResponse("/welcome", status_code=303)
    database.delete_user_sessions(user_id)
    response = RedirectResponse("/welcome?info=logged_out", status_code=303)
    response.delete_cookie(SESSION_COOKIE)
    return response


@app.post("/security/delete-data")
async def security_delete_data(request: Request, confirm_text: str = Form("")):
    user_id = current_user(request)
    if user_id is None:
        return RedirectResponse("/welcome", status_code=303)
    if confirm_text.strip() != "DELETE":
        return RedirectResponse("/security?error=confirm", status_code=303)

    database.delete_user_data(user_id)
    for path in glob.glob(os.path.join(CHARTS_DIR, f"{user_id}_*.png")):
        os.remove(path)

    response = RedirectResponse("/welcome?info=deleted", status_code=303)
    response.delete_cookie(SESSION_COOKIE)
    return response


@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return FileResponse("web/static/logo-icon.png")

# ---------- API: чат с агентом ----------

@app.post("/api/chat")
async def api_chat(request: Request, body: ChatRequest):
    user_id = current_user(request)
    if user_id is None:
        return JSONResponse({"error": "unauthorized"}, status_code=401)

    text = body.message.strip()[:1000]

    # 🔐 Номер карты не уходит в модель (как в боте)
    if security.find_card_numbers(text):
        return {"reply": tr(request, "🚫 Your message contained a card number, so it was not sent. "
                                     "Never share card numbers, CVV or PIN — not even with me."),
                "steps": [], "images": [], "confirmations": []}

    # Собираем шаги агента, чтобы показать их на странице
    steps = []

    async def on_tool_call(name):
        steps.append(name)

    reply, images, confirmations = await run_agent(user_id, text, on_tool_call=on_tool_call)

    # 🔐 Подтверждения храним у себя, наружу отдаём только случайный код
    confirmation_list = []
    for conf in confirmations:
        token = secrets.token_urlsafe(16)
        PENDING[token] = {"user_id": user_id, "data": conf, "created": time.time()}
        confirmation_list.append({
            "token": token,
            "text": tr(request, "🔐 Remove limit? {scope}: {target} — {amount} ₼",
                       scope=tr(request, "Card" if conf["scope"] == "card" else "Category"),
                       target=tr(request, CATEGORY_INFO[conf["target"]][1])
                       if conf["target"] in CATEGORY_INFO else conf["target"],
                       amount=conf["amount"]),
        })

    return {
        "reply": reply,
        "steps": steps,
        "images": [f"/charts/{os.path.basename(p)}?v={int(time.time())}" for p in images],
        "confirmations": confirmation_list,
    }


@app.post("/api/confirm")
async def api_confirm(request: Request, body: ConfirmRequest):
    user_id = current_user(request)
    if user_id is None:
        return JSONResponse({"error": "unauthorized"}, status_code=401)

    item = PENDING.pop(body.token, None)
    if item is None or item["user_id"] != user_id:
        return {"message": tr(request, "⚠️ Request not found")}
    if time.time() - item["created"] > CONFIRM_TTL_SECONDS:
        return {"message": tr(request, "⌛ Request expired")}
    if body.action != "confirm":
        return {"message": tr(request, "❌ Cancelled")}

    conf = item["data"]
    if conf["action"] == "remove_limit":
        removed = database.remove_limit(user_id, conf["scope"], conf["target"])
        return {"message": tr(request, "✅ Limit removed" if removed else "⚠️ Limit not found")}
    return {"message": tr(request, "⚠️ Unknown action")}


@app.get("/charts/{filename}")
async def chart_image(request: Request, filename: str):
    user_id = current_user(request)
    # 🔐 Только свои графики: имя файла начинается с твоего Telegram ID
    if user_id is None or not filename.startswith(f"{user_id}_"):
        return JSONResponse({"error": "forbidden"}, status_code=403)
    path = os.path.join(CHARTS_DIR, os.path.basename(filename))
    if not os.path.exists(path):
        return JSONResponse({"error": "not found"}, status_code=404)
    return FileResponse(path, headers={"Cache-Control": "no-store"})