from pathlib import Path
from typing import Optional

from fastapi import APIRouter, Request

from models.tariff import TariffModel
from schemas.tariff import TariffSchema

router = APIRouter(prefix=f"/{Path(__file__).stem}", tags=[Path(__file__).stem])


@router.get("/get_tarif")
async def get_tarif(request: Request) -> Optional[TariffSchema]:
    user = request.state.user
    if user.tariff_id:
        return TariffSchema.model_validate(user.tariff)
    return None
