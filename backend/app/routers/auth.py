from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.db import get_db
from app.models.models import User
from app.core.security import create_access_token
from pydantic import BaseModel

router = APIRouter()

class OTPRequest(BaseModel):
    phone: str

class OTPVerify(BaseModel):
    phone: str
    otp: str

@router.post("/request-otp")
async def request_otp(payload: OTPRequest):
    # Simulation: send SMS
    return {"message": "OTP sent successfully"}

@router.post("/verify-otp")
async def verify_otp(payload: OTPVerify, db: AsyncSession = Depends(get_db)):
    if payload.otp != "123456":
        raise HTTPException(status_code=400, detail="Invalid OTP")

    result = await db.execute(select(User).where(User.phone == payload.phone))
    user = result.scalars().first()

    if not user:
        user = User(phone=payload.phone, roles=["driver"])
        db.add(user)
        await db.flush()

    access_token = create_access_token(data={"sub": user.phone})
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {"phone": user.phone, "name": user.name, "roles": user.roles}
    }
