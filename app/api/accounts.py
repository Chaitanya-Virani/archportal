from fastapi import APIRouter, Depends, HTTPException, status, Response, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from app.core.security import get_current_user
from app.core.supabase import supabase
from app.core.config import settings
from app.core.templates import templates

router = APIRouter(prefix="/accounts", tags=["accounts"])

@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@router.post("/login")
async def login(response: Response, request: Request, email: str = Form(...), password: str = Form(...)):
    try:
        # Supabase Auth login
        auth_res = supabase.auth.sign_in_with_password({"email": email, "password": password})
        token = auth_res.session.access_token

        # Set secure HTTP-only cookie and redirect to dashboard
        redirect = RedirectResponse(url="/", status_code=302)
        redirect.set_cookie(key="supabase-token", value=token, httponly=True, secure=True, samesite="Lax")
        return redirect
    except Exception as e:
        return templates.TemplateResponse("login.html", {
            "request": request,
            "error": str(e)
        }, status_code=401)

@router.get("/logout")
async def logout(response: Response):
    # Clear cookie and redirect to login
    redirect = RedirectResponse(url="/accounts/login", status_code=302)
    redirect.delete_cookie("supabase-token")
    return redirect

@router.get("/profile")
async def get_profile(user = Depends(get_current_user)):
    res = supabase.table("profiles").select("*").eq("id", user.id).single().execute()
    return res.data

@router.patch("/profile")
async def update_profile(full_name: str, avatar_url: str = None, user = Depends(get_current_user)):
    res = supabase.table("profiles").update({"full_name": full_name, "avatar_url": avatar_url}).eq("id", user.id).execute()
    return res.data
