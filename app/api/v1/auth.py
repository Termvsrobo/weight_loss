from pathlib import Path
from typing import Optional

from fastapi import APIRouter
from pydantic import SecretStr, EmailStr

from app.schemas.user import PhoneModel, UserModel


router = APIRouter(prefix=f"/{Path(__file__).stem}", tags=[Path(__file__).stem])


@router.post("/send_sms_code")
async def send_sms_code(phone: PhoneModel):
    return True


@router.post("/verify_sms_code")
async def verify_sms_code(phone: PhoneModel, code: str):
    return code == "123456"


@router.post("/login")
async def login(phone: PhoneModel, password: SecretStr):
    return UserModel()


@router.post("/register")
async def register(
    phone: PhoneModel, password: SecretStr, email: Optional[EmailStr] = None
):
    return UserModel()
