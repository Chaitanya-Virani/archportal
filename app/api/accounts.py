from fastapi import APIRouter, Depends, HTTPException, status, Response
from app.core.security import get_current_user, role_required
from app.core.supabase import supabase
from app.core.config import settings

router = APIRouter(prefix="/accounts", tags=["accounts"])

@router.post("/login")
async def login(response: Response, username: str, password: str):
    try:
        # Supabase Auth login
        auth_res = supabase.auth.sign_in_with_password({"email": username, "password": password})
        token = auth_res.session.access_token

        # Set secure HTTP-only cookie
        response.set_cookie(key="supabase-token", value=token, httponly=True, secure=True, samesite="Lax")
        return {"status": "success", "message": "Logged in successfully"}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))

@router.post("/logout")
async def logout(response: Response):
    # Clear cookie
    response.delete_cookie("supabase-token")
    return {"status": "success", "message": "Logged out successfully"}

@router.get("/profile")
async def get_profile(user = Depends(get_current_user)):
    res = supabase.table("profiles").select("*").eq("id", user.id).single().execute()
    return res.data

@router.patch("/profile")
async def update_profile(full_name: str, avatar_url: str = None, user = Depends(get_current_user)):
    res = supabase.table("profiles").update({"full_name": full_name, "avatar_url": avatar_url}).eq("id", user.id).execute()
    return res.data
