from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

import database

app = FastAPI(title="Fintra")
templates = Jinja2Templates(directory="web/templates")


@app.on_event("startup")
def startup():
    database.init_db()


# ---------- Страницы ----------

@app.get("/", response_class=HTMLResponse)
async def overview(request: Request):
    return templates.TemplateResponse(request, "overview.html", {"active": "overview"})


@app.get("/expenses", response_class=HTMLResponse)
async def expenses(request: Request):
    return templates.TemplateResponse(request, "expenses.html", {"active": "expenses"})


@app.get("/plan", response_class=HTMLResponse)
async def plan(request: Request):
    return templates.TemplateResponse(request, "plan.html", {"active": "plan"})


@app.get("/chat", response_class=HTMLResponse)
async def chat(request: Request):
    return templates.TemplateResponse(request, "chat.html", {"active": "chat"})


@app.get("/security", response_class=HTMLResponse)
async def security_page(request: Request):
    return templates.TemplateResponse(request, "security.html", {"active": "security"})