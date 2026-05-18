from fastapi import APIRouter, Depends, HTTPException, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from app.core.security import get_current_user, role_required
from app.core.supabase import supabase
from app.core.templates import templates

router = APIRouter(prefix="/employees", tags=["employees"])

@router.get("/", response_class=HTMLResponse)
async def list_employees(request: Request, user = Depends(get_current_user)):
    res = supabase.table("employees").select("*").execute()
    employees = res.data
    return templates.TemplateResponse(request, "employees_list.html", {
        "employees": employees,
        "user": user,
        "active_page": "employees"
    })

@router.get("/{employee_id}", response_class=HTMLResponse)
async def employee_detail(request: Request, employee_id: str, user = Depends(get_current_user)):
    # Fetch employee and their assigned projects
    emp_res = supabase.table("employees").select("*").eq("id", employee_id).single().execute()
    employee = emp_res.data

    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    # Fetch assigned projects via project_assignments table
    assign_res = supabase.table("project_assignments").select("project_id").eq("employee_id", employee_id).execute()
    project_ids = [a['project_id'] for a in assign_res.data]

    projects = []
    if project_ids:
        proj_res = supabase.table("projects").select("*").in_("id", project_ids).execute()
        projects = proj_res.data

    return templates.TemplateResponse(request, "employee_detail.html", {
        "employee": employee,
        "projects": projects,
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
    return RedirectResponse(url="/employees/", status_code=303)
