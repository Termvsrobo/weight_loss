from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class ChallengeSchema(BaseModel):
    id: Optional[int] = None
    title: str
    start: datetime
    end: datetime
    prize: str
    joined: bool

    model_config = ConfigDict(from_attributes=True)


class ChallengeJoinSchema(BaseModel):
    challenge_id: int
