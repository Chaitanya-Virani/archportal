from fastapi import FastAPI, Request, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from app.core.config import settings
from app.api import accounts, employees, projects, billing, dashboard
from app.core.security import get_current_user

app = FastAPI(title="ArchPortal Management System")

# Mount static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Setup templates
templates = Jinja2Templates(directory="app/templates")

# Include Routers
app.include_router(accounts.router)
app.include_router(employees.router)
app.include_router(projects.router)
app.include_router(billing.router)
app.include_router(dashboard.router)

@app.get("/", response_class=HTMLResponse)
async def root(request: Request, user = Depends(get_current_user)):
    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "user": user,
        "active_page": "dashboard"
    })
