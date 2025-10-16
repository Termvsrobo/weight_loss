from datetime import datetime
from enum import StrEnum
from typing import Optional

from pydantic import BaseModel, ConfigDict


class WeightStatusType(StrEnum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"


class WeightLogSchema(BaseModel):
    date: datetime
    weight: float
    media_url: Optional[str] = None
    status: WeightStatusType

    model_config = ConfigDict(from_attributes=True)
