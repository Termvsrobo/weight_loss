from pathlib import Path

from fastapi import APIRouter

from models.transaction import TransactionModel
from schemas.transaction import TransactionSchema

router = APIRouter(prefix=f"/{Path(__file__).stem}", tags=[Path(__file__).stem])


@router.get("/get_transactions")
async def get_transactions() -> list[TransactionSchema]:
    result = []
    for transaction in sorted(TransactionModel.filter().all(), key=lambda x: x.id):
        result.append(TransactionSchema.model_validate(transaction))
    return result
