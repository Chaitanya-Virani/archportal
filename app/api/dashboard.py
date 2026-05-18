from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse
from app.core.security import get_current_user
from app.core.supabase import supabase
from app.core.templates import templates

router = APIRouter(prefix="/dashboard", tags=["dashboard"])

@router.get("/", response_class=HTMLResponse)
async def dashboard(request: Request, user = Depends(get_current_user)):
    # Default values in case tables don't exist or queries fail
    active_projects = 0
    pending_receivables = 0
    active_architects = 0
    recent_projects = []
    upcoming_deadlines = []

    try:
        # 1. Total active projects
        proj_res = supabase.table("projects").select("id", count="exact").eq("status", "IN_PROGRESS").execute()
        active_projects = proj_res.count or 0
    except Exception:
        pass

    try:
        # 2. Total pending receivables (Sum of all PENDING and OVERDUE invoices)
        inv_res = supabase.table("invoices").select("amount").in_("status", ["PENDING", "OVERDUE"]).execute()
        pending_receivables = sum(inv.get('amount', 0) or 0 for inv in inv_res.data)
    except Exception:
        pass

    try:
        # 3. Total Architects
        emp_res = supabase.table("employees").select("id", count="exact").eq("is_active", True).execute()
        active_architects = emp_res.count or 0
    except Exception:
        pass

    try:
        # 4. Recent Projects (Top 5)
        recent_proj = supabase.table("projects").select("*").order("created_at", desc=True).limit(5).execute()
        recent_projects = recent_proj.data
    except Exception:
        pass

    try:
        # 5. Upcoming Deadlines (Next 30 days)
        deadlines = supabase.table("projects").select("name, deadline").order("deadline", asc=True).limit(5).execute()
        upcoming_deadlines = deadlines.data
    except Exception:
        pass

    return templates.TemplateResponse(request, "dashboard.html", {
        "user": user,
        "active_page": "dashboard",
        "stats": {
            "active_projects": active_projects,
            "pending_receivables": pending_receivables,
            "active_architects": active_architects
        },
        "recent_projects": recent_projects,
        "upcoming_deadlines": upcoming_deadlines
    })
