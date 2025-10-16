from pathlib import Path

from fastapi import APIRouter

from models.tariff import TariffModel
from schemas.tariff import TariffSchema

router = APIRouter(prefix=f"/{Path(__file__).stem}", tags=[Path(__file__).stem])


@router.get("/get_tarif")
async def get_tarif() -> list[TariffSchema]:
    return [
        TariffSchema.model_validate(tariff) for tariff in TariffModel.filter().all()
    ]
