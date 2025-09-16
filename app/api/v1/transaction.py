from pathlib import Path

from fastapi import APIRouter


router = APIRouter(prefix=f"/{Path(__file__).stem}", tags=[Path(__file__).stem])


@router.get("/get_transactions")
async def get_transactions() -> list:
    return []
