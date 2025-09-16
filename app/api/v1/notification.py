from pathlib import Path

from fastapi import APIRouter


router = APIRouter(prefix=f"/{Path(__file__).stem}", tags=[Path(__file__).stem])


@router.get("/get_preferences")
async def get_preferences():
    return {
        "motivation": True,
        "reminders": True,
        "accruals": False,
    }


@router.post("/set_preferences")
async def set_preferences():
    return True
