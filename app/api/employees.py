from fastapi import APIRouter, Depends, HTTPException, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from app.core.security import get_current_user, role_required
from app.core.supabase import supabase
from app.main import templates

router = APIRouter(prefix="/employees", tags=["employees"])

@router.get("/", response_class=HTMLResponse)
async def list_employees(request: Request, user = Depends(get_current_user)):
    res = supabase.table("employees").select("*").execute()
    employees = res.data
    return templates.TemplateResponse("employees_list.html", {
        "request": request,
        "employees": employees,
        "user": user,
        "active_page": "employees"
    })

@router.get("/{employee_id}", response_class=HTMLResponse)
async def employee_detail(request: Request, employee_id: str, user = Depends(get_current_user)):
    res = supabase.table("employees").select("*").eq("id", employee_id).single().execute()
    employee = res.data
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    return templates.TemplateResponse("employee_detail.html", {
        "request": request,
        "employee": employee,
        "user": user,
        "active_page": "employees"
    })

@router.post("/create")
async def create_employee(
    request: Request,
    name: str = Form(...),
    email: str = Form(...),
    role_title: str = Form(...),
    user = Depends(get_current_user),
    role = Depends(role_required(["ADMIN"]))
):
    data = {
        "name": name,
        "email": email,
        "role_title": role_title,
        "is_active": True
    }
    res = supabase.table("employees").insert(data).execute()
    return templates.TemplateResponse("employees_list.html", {
        "request": request,
        "employees": res.data,
        "user": user,
        "active_page": "employees"
    })
