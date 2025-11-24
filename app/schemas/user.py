from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr, NonNegativeFloat, SecretStr
from pydantic_extra_types.phone_numbers import PhoneNumber


class PhoneMixin:
    phone: PhoneNumber

    def __init__(self, **data):
        if "phone" in data and data["phone"]:
            if data["phone"].startswith("8"):
                data["phone"] = f"+7{data['phone'][1:]}"
            for sym in ("-", " ", "(", ")"):
                data["phone"] = data["phone"].replace(sym, "")
        super().__init__(**data)


class PhoneModel(PhoneMixin, BaseModel): ...


class UserSchema(PhoneMixin, BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    country: Optional[str] = None
    telegram: Optional[str] = None
    avatar_url: Optional[str] = None
    tariff_status: Optional[str] = None
    deposit: Optional[float] = None

    model_config = ConfigDict(from_attributes=True)


class UserUpdateSchema(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    country: Optional[str] = None
    telegram: Optional[str] = None
    avatar_url: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class UserRegisterSchema(PhoneMixin, BaseModel):
    password: SecretStr
    email: Optional[EmailStr] = None


class UserLoginSchema(PhoneMixin, BaseModel):
    password: SecretStr


class AmountSchema(BaseModel):
    amount: NonNegativeFloat


class SmsCodeSchema(PhoneMixin, BaseModel):
    code: str
