from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

import database

app = FastAPI(title="Fintra")
templates = Jinja2Templates(directory="web/templates")
app.mount("/static", StaticFiles(directory="web/static"), name="static")

SESSION_COOKIE = "fintra_session"
SESSION_HOURS = 24


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


# ---------- Страницы ----------

@app.get("/", response_class=HTMLResponse)
async def overview(request: Request):
    return render_page(request, "overview.html", "overview")


@app.get("/expenses", response_class=HTMLResponse)
async def expenses(request: Request):
    return render_page(request, "expenses.html", "expenses")


@app.get("/plan", response_class=HTMLResponse)
async def plan(request: Request):
    return render_page(request, "plan.html", "plan")


@app.get("/chat", response_class=HTMLResponse)
async def chat(request: Request):
    return render_page(request, "chat.html", "chat")


@app.get("/security", response_class=HTMLResponse)
async def security_page(request: Request):
    return render_page(request, "security.html", "security")