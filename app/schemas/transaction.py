from typing import Optional
from enum import StrEnum
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class TransactionType(StrEnum):
    REFILL = "Пополнение"
    ACCRUAL = "Начисление"
    WITHDRAWAL = "Вывод"


class TransactionSchema(BaseModel):
    id: Optional[int] = None
    type: TransactionType
    amount: float
    date: datetime

    model_config = ConfigDict(from_attributes=True)
