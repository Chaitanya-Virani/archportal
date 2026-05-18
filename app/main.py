from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.core.config import settings
from app.api import accounts, employees

app = FastAPI(title="ArchPortal Management System")

# Mount static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Setup templates
templates = Jinja2Templates(directory="app/templates")

# Include Routers
app.include_router(accounts.router)
app.include_router(employees.router)

@app.get("/")
async def root():
    return {"message": "Welcome to ArchPortal API. UI templates are under integration."}
