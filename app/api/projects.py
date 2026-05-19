from fastapi import APIRouter, Depends, HTTPException, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from app.core.security import get_current_user, role_required
from app.core.supabase import supabase
from app.core.templates import templates

router = APIRouter(prefix="/projects", tags=["projects"])

@router.get("/", response_class=HTMLResponse)
async def list_projects(request: Request, user = Depends(get_current_user)):
    res = supabase.table("projects").select("*").execute()
    projects = res.data
    return templates.TemplateResponse(request, "projects_list.html", {
        "projects": projects,
        "user": user,
        "active_page": "projects"
    })

@router.get("/{project_id}", response_class=HTMLResponse)
async def project_detail(request: Request, project_id: str, user = Depends(get_current_user)):
    try:
        proj_res = supabase.table("projects").select("*").eq("id", project_id).single().execute()
        project = proj_res.data
    except Exception:
        raise HTTPException(status_code=404, detail="Project not found")

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    # Fetch assigned architects (safely — table may not exist)
    architects = []
    try:
        assign_res = supabase.table("project_assignments").select("employee_id").eq("project_id", project_id).execute()
        employee_ids = [a['employee_id'] for a in assign_res.data]
        if employee_ids:
            emp_res = supabase.table("employees").select("*").in_("id", employee_ids).execute()
            architects = emp_res.data
    except Exception:
        pass

    # Fetch project invoices (safely)
    invoices = []
    try:
        inv_res = supabase.table("invoices").select("*").eq("project_id", project_id).execute()
        invoices = inv_res.data
    except Exception:
        pass

    total_budget = project.get('budget', 0) or 0
    total_invoiced = sum(inv.get('amount', 0) or 0 for inv in invoices)
    invoiced_percent = round((total_invoiced / total_budget * 100), 1) if total_budget > 0 else 0

    # Normalize phase field: the create endpoint stores "phase",
    # but some code/templates may expect "current_phase".
    if 'current_phase' not in project and 'phase' in project:
        project['current_phase'] = project['phase']
    elif 'phase' not in project and 'current_phase' in project:
        project['phase'] = project['current_phase']
    # Ensure both keys exist with a sensible default
    project.setdefault('phase', 'SD')
    project.setdefault('current_phase', project['phase'])

    return templates.TemplateResponse(request, "project_detail.html", {
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
        "current_phase": "SD",
        "created_by": user.id
    }
    res = supabase.table("projects").insert(data).execute()
    return RedirectResponse(url="/projects/", status_code=303)

@router.post("/assign")
async def assign_architect(
    project_id: str = Form(...),
    employee_id: str = Form(...),
    user = Depends(get_current_user),
    role = Depends(role_required(["ADMIN"]))
):
    try:
        supabase.table("project_assignments").insert({
            "project_id": project_id,
            "employee_id": employee_id,
        }).execute()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    return RedirectResponse(url=f"/projects/{project_id}", status_code=303)
