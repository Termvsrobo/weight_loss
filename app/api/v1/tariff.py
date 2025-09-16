from pathlib import Path

from fastapi import APIRouter


router = APIRouter(prefix=f"/{Path(__file__).stem}", tags=[Path(__file__).stem])


@router.get("/get_tarif")
async def get_tarif() -> list:
    return []
