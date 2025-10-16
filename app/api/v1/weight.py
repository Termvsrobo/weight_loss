from pathlib import Path

from fastapi import APIRouter, Request

from models.weight import WeightLogModel
from schemas.weight import WeightLogSchema

router = APIRouter(prefix=f"/{Path(__file__).stem}", tags=[Path(__file__).stem])


@router.get("/get_history")
async def get_history(request: Request) -> list[WeightLogSchema]:
    result = []
    for transaction in sorted(
        WeightLogModel.filter(user_id=request.state.user.id).all(), key=lambda x: x.id
    ):
        result.append(WeightLogSchema.model_validate(transaction))
    return result


@router.post("/submit_weight")
async def submit_weight(request: Request, weight: WeightLogSchema):
    weight_log = WeightLogModel(user_id=request.state.user.id, **weight.model_dump())
    is_ok, error = weight_log.save()
    return is_ok


@router.post("/generate_session_code")
async def generate_session_code():
    return "KP-${DateTime.now().millisecondsSinceEpoch.toString().substring(8)}"
