from fastapi import FastAPI, Request, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, RedirectResponse
from app.core.config import settings
from app.core.templates import templates
from app.core.security import get_current_user_optional
import os

app = FastAPI(title="ArchPortal Management System")

# Mount static files (create dir if missing, e.g. on Render)
_static_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static")
os.makedirs(_static_dir, exist_ok=True)
app.mount("/static", StaticFiles(directory=_static_dir), name="static")

# Import and include routers AFTER app is created to avoid circular imports
from app.api import accounts, employees, projects, billing, dashboard

app.include_router(accounts.router)
app.include_router(employees.router)
app.include_router(projects.router)
app.include_router(billing.router)
app.include_router(dashboard.router)

@app.get("/", response_class=HTMLResponse)
async def root(request: Request, user = Depends(get_current_user_optional)):
    if not user:
        return RedirectResponse(url="/accounts/login", status_code=302)
    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "user": user,
        "active_page": "dashboard"
    })
