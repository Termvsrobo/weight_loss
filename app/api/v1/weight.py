from pathlib import Path
from typing import Optional

from fastapi import APIRouter


router = APIRouter(prefix=f"/{Path(__file__).stem}", tags=[Path(__file__).stem])


@router.get("/get_history")
async def get_history():
    return []


@router.post("/submit_weight")
async def submit_weight(weight: float, code: str, media_path: Optional[str] = None):
    return True


@router.post("/generate_session_code")
async def generate_session_code():
    return "KP-${DateTime.now().millisecondsSinceEpoch.toString().substring(8)}"
