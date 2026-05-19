from fastapi import APIRouter, Depends, HTTPException, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from app.core.security import get_current_user, role_required
from app.core.supabase import supabase
from app.core.templates import templates
from datetime import date

router = APIRouter(prefix="/billing", tags=["billing"])


def _normalize_invoice(inv):
    """Flatten the nested projects join into a top-level project_name field."""
    if inv and 'projects' in inv and isinstance(inv['projects'], dict):
        inv['project_name'] = inv['projects'].get('name', '')
    elif inv and 'project_name' not in inv:
        inv['project_name'] = ''
    # Ensure issue_date has a fallback
    inv.setdefault('issue_date', inv.get('created_at', 'N/A'))
    return inv


@router.get("/", response_class=HTMLResponse)
async def list_invoices(request: Request, user = Depends(get_current_user)):
    try:
        res = supabase.table("invoices").select("*, projects(name)").execute()
        invoices = [_normalize_invoice(inv) for inv in res.data]
    except Exception:
        invoices = []

    try:
        proj_res = supabase.table("projects").select("id, name").execute()
        projects = proj_res.data
    except Exception:
        projects = []

    return templates.TemplateResponse(request, "billing_list.html", {
        "invoices": invoices,
        "projects": projects,
        "user": user,
        "active_page": "billing"
    })

@router.get("/{invoice_id}", response_class=HTMLResponse)
async def invoice_detail(request: Request, invoice_id: str, user = Depends(get_current_user)):
    try:
        res = supabase.table("invoices").select("*, projects(name)").eq("id", invoice_id).single().execute()
        invoice = _normalize_invoice(res.data)
    except Exception:
        raise HTTPException(status_code=404, detail="Invoice not found")

    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")

    return templates.TemplateResponse(request, "billing_detail.html", {
        "invoice": invoice,
        "user": user,
        "active_page": "billing"
    })

@router.post("/create")
async def create_invoice(
    request: Request,
    project_id: str = Form(...),
    invoice_number: str = Form(...),
    amount: float = Form(...),
    due_date: str = Form(...),
    user = Depends(get_current_user),
    role = Depends(role_required(["ADMIN", "ACCOUNTANT"]))
):
    data = {
        "project_id": project_id,
        "invoice_number": invoice_number,
        "amount": amount,
        "due_date": due_date,
        "issue_date": str(date.today()),
        "status": "PENDING",
        "created_by": user.id
    }
    res = supabase.table("invoices").insert(data).execute()
    return RedirectResponse(url="/billing/", status_code=303)

@router.post("/mark-paid/{invoice_id}")
async def mark_paid(invoice_id: str, user = Depends(get_current_user), role = Depends(role_required(["ADMIN", "ACCOUNTANT"]))):
    res = supabase.table("invoices").update({"status": "PAID"}).eq("id", invoice_id).execute()
    return RedirectResponse(url=f"/billing/{invoice_id}", status_code=303)
