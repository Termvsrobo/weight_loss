from pathlib import Path

from fastapi import APIRouter

router = APIRouter(prefix=f"/{Path(__file__).stem}", tags=[Path(__file__).stem])


@router.get("/get_challenges")
async def get_challenges() -> list:
    return []


@router.post("/join")
async def challenge_join(challenge_id: int):
    return True
