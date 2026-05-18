from fastapi import Request, HTTPException, Depends, status
from fastapi.responses import Response
from app.core.config import settings
from app.core.supabase import supabase
from typing import Optional
import jwt

def get_token_from_cookie(request: Request) -> Optional[str]:
    return request.cookies.get("supabase-token")

async def get_current_user(token: str = Depends(get_token_from_cookie)):
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )

    try:
        # Verify token with Supabase
        user = supabase.auth.get_user(token)
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
        return user.user
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))

async def get_current_user_role(user = Depends(get_current_user)):
    # Fetch role from profiles table
    res = supabase.table("profiles").select("role").eq("id", user.id).single().execute()
    if not res.data:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Profile not found or role not assigned"
        )
    return res.data['role']

def role_required(allowed_roles: list[str]):
    async def role_checker(role: str = Depends(get_current_user_role)):
        if role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Operation requires one of these roles: {allowed_roles}"
            )
        return role
    return role_checker
