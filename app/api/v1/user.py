from pathlib import Path

from fastapi import APIRouter

from app.schemas.user import UserModel


router = APIRouter(prefix=f"/{Path(__file__).stem}", tags=[Path(__file__).stem])


@router.get("/get_balance")
async def get_balance() -> float:
    return 4800.0


@router.post("/top_up")
async def top_up(amount: float) -> bool:
    return True


@router.get("/get_profile")
async def get_profile():
    return UserModel()


@router.post("/update_profile")
async def update_profile(updated: UserModel):
    return updated
