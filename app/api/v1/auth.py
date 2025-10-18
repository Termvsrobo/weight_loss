from pathlib import Path

from fastapi import APIRouter, HTTPException, status

from models.user import UserModel
from schemas.auth import AccessToken
from schemas.user import PhoneModel, UserSchema, UserRegisterSchema, UserLoginSchema, SmsCodeSchema
from services.auth_service import get_access_refresh_token

router = APIRouter(prefix=f"/{Path(__file__).stem}", tags=[Path(__file__).stem])


@router.post("/send_sms_code")
async def send_sms_code(phone: PhoneModel):
    return True


@router.post("/verify_sms_code")
async def verify_sms_code(phone: SmsCodeSchema):
    return phone.code == "123456"


@router.post("/login")
async def login(user_login: UserLoginSchema):
    user = UserModel.filter(phone=user_login.phone).first()
    if user:
        if user.check_password(user_login.password.get_secret_value()):
            access_token, refresh_token = get_access_refresh_token(user)
            return AccessToken(access_token=access_token, refresh_token=refresh_token)

    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Could not validate credentials',
        headers={'WWW-Authenticate': 'Bearer'},
    )


@router.post("/register")
async def register(user_register: UserRegisterSchema):
    user = UserModel(**user_register.model_dump(exclude=["password"]))
    user.set_password(user_register.password.get_secret_value())
    is_ok, _ = user.create()
    if is_ok:
        model_user = UserSchema.model_validate(user)
        return model_user
    else:
        return "Пользователь с таким номером уже существует"
