from pathlib import Path

from fastapi import APIRouter, Request

from schemas.user import UserSchema, AmountSchema, UserUpdateSchema
from models.user import UserModel

router = APIRouter(prefix=f"/{Path(__file__).stem}", tags=[Path(__file__).stem])


@router.get("/get_balance")
async def get_balance(request: Request) -> float:
    return request.state.user.deposit or 0


@router.post("/top_up")
async def top_up(request: Request, amount: AmountSchema) -> bool:
    request.state.user.top_up(amount.amount)
    return True


@router.get("/get_profile")
async def get_profile(request: Request) -> UserSchema:
    return UserSchema.model_validate(request.state.user)


@router.post("/update_profile")
async def update_profile(request: Request, updated: UserUpdateSchema) -> UserSchema:
    new_date = updated.model_dump(exclude_defaults=True, exclude_none=True)
    if new_date:
        UserModel.update(new_date, id=request.state.user.id)
        request.state.user.refresh_from_db()
    return UserSchema.model_validate(request.state.user)
