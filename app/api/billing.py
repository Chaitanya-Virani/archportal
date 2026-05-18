from fastapi import APIRouter, Depends, HTTPException, Request, Form
from fastapi.responses import HTMLResponse
from app.core.security import get_current_user, role_required
from app.core.supabase import supabase
from app.core.templates import templates
from datetime import date

router = APIRouter(prefix="/billing", tags=["billing"])

@router.get("/", response_class=HTMLResponse)
async def list_invoices(request: Request, user = Depends(get_current_user)):
    res = supabase.table("invoices").select("*, projects(name)").execute()
    invoices = res.data
    return templates.TemplateResponse("billing_list.html", {
        "request": request,
        "invoices": invoices,
        "user": user,
        "active_page": "billing"
    })

@router.get("/{invoice_id}", response_class=HTMLResponse)
async def invoice_detail(request: Request, invoice_id: str, user = Depends(get_current_user)):
    res = supabase.table("invoices").select("*, projects(name)").eq("id", invoice_id).single().execute()
    invoice = res.data
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")

    return templates.TemplateResponse("billing_detail.html", {
        "request": request,
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
        "status": "PENDING",
        "created_by": user.id
    }
    res = supabase.table("invoices").insert(data).execute()
    return templates.TemplateResponse("billing_list.html", {
        "request": request,
        "invoices": res.data,
        "user": user,
        "active_page": "billing"
    })

@router.post("/mark-paid/{invoice_id}")
async def mark_paid(invoice_id: str, user = Depends(get_current_user), role = Depends(role_required(["ADMIN", "ACCOUNTANT"]))):
    res = supabase.table("invoices").update({"status": "PAID"}).eq("id", invoice_id).execute()
    return {"status": "success", "message": "Invoice marked as paid"}
