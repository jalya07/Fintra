from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

import database

app = FastAPI(title="Fintra")
templates = Jinja2Templates(directory="web/templates")


@app.on_event("startup")
def startup():
    database.init_db()


@app.get("/", response_class=HTMLResponse)
async def overview(request: Request):
    return templates.TemplateResponse(request, "overview.html", {})