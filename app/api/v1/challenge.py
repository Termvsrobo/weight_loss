from pathlib import Path

from fastapi import APIRouter, Request

from models.challenge import ChallengeModel
from schemas.challenge import ChallengeJoinSchema, ChallengeSchema

router = APIRouter(prefix=f"/{Path(__file__).stem}", tags=[Path(__file__).stem])


@router.get("/get_challenges")
async def get_challenges(request: Request) -> list[ChallengeSchema]:
    result = []
    for challenge in sorted(ChallengeModel.filter().all(), key=lambda x: x.id):
        challenge.joined = request.state.user in challenge.users
        result.append(ChallengeSchema.model_validate(challenge))
    return result


@router.post("/join")
async def challenge_join(request: Request, challenge_id: ChallengeJoinSchema):
    challenge = ChallengeModel.filter(id=challenge_id.challenge_id).first()
    if challenge:
        challenge.join(request.state.user)
        return True
    return False
