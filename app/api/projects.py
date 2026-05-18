from fastapi import APIRouter, Depends, HTTPException, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from app.core.security import get_current_user, role_required
from app.core.supabase import supabase
from app.main import templates

router = APIRouter(prefix="/projects", tags=["projects"])

@router.get("/", response_class=HTMLResponse)
async def list_projects(request: Request, user = Depends(get_current_user)):
    res = supabase.table("projects").select("*").execute()
    projects = res.data
    return templates.TemplateResponse("projects_list.html", {
        "request": request,
        "projects": projects,
        "user": user,
        "active_page": "projects"
    })

@router.get("/{project_id}", response_class=HTMLResponse)
async def project_detail(request: Request, project_id: str, user = Depends(get_current_user)):
    proj_res = supabase.table("projects").select("*").eq("id", project_id).single().execute()
    project = proj_res.data
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    # Fetch assigned architects
    assign_res = supabase.table("project_assignments").select("employee_id").eq("project_id", project_id).execute()
    employee_ids = [a['employee_id'] for a in assign_res.data]

    architects = []
    if employee_ids:
        emp_res = supabase.table("employees").select("*").in_("id", employee_ids).execute()
        architects = emp_res.data

    # Fetch project invoices
    inv_res = supabase.table("invoices").select("*").eq("project_id", project_id).execute()
    invoices = inv_res.data

    # Calculate financial stats
    total_budget = project.get('budget', 0) or 0
    total_invoiced = sum(inv.get('amount', 0) or 0 for inv in invoices)
    invoiced_percent = round((total_invoiced / total_budget * 100), 1) if total_budget > 0 else 0

    return templates.TemplateResponse("project_detail.html", {
        "request": request,
        "project": project,
        "architects": architects,
        "invoices": invoices,
        "total_invoiced": total_invoiced,
        "invoiced_percent": invoiced_percent,
        "user": user,
        "active_page": "projects"
    })

@router.post("/create")
async def create_project(
    request: Request,
    name: str = Form(...),
    client_name: str = Form(...),
    location: str = Form(None),
    budget: float = Form(0.0),
    deadline: str = Form(...),
    user = Depends(get_current_user),
    role = Depends(role_required(["ADMIN", "ARCHITECT"]))
):
    data = {
        "name": name,
        "client_name": client_name,
        "location": location,
        "budget": budget,
        "deadline": deadline,
        "status": "PLANNING",
        "phase": "SD",
        "created_by": user.id
    }
    res = supabase.table("projects").insert(data).execute()
    return templates.TemplateResponse("projects_list.html", {
        "request": request,
        "projects": res.data,
        "user": user,
        "active_page": "projects"
    })
