from typing import Optional

from pydantic import BaseModel, ConfigDict


class TariffSchema(BaseModel):
    name: str
    percent: int
    description: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)
