from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session
from passlib.context import CryptContext

from app.api.dependencies import get_db
from app.db import models

router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class LoginRequest(BaseModel):
    email: str
    password: str


class LoginResponse(BaseModel):
    access_token: str
    token_type: str
    user: dict


@router.get("/test")
def test_auth():
    return {"message": "Authentication route is working"}


@router.post("/login")
def login(credentials: LoginRequest, db: Session = Depends(get_db)):
    """
    Demo login endpoint.
    Validates email/password against the users table and returns user info
    with a simple token (not full JWT — just enough for the demo).
    """
    user = db.query(models.User).filter(
        models.User.email == credentials.email
    ).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    if not pwd_context.verify(credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account is inactive",
        )

    return LoginResponse(
        access_token=f"demo_token_{user.id}",
        token_type="bearer",
        user={
            "id": user.id,
            "email": user.email,
            "full_name": user.full_name,
            "is_active": user.is_active,
        },
    )