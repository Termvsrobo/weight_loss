from datetime import datetime

from sqlalchemy import DateTime, Float, String
from sqlalchemy.orm import Mapped, mapped_column

from database import Base


class TransactionModel(Base):
    __tablename__ = "transactions"
    id: Mapped[int] = mapped_column(primary_key=True)
    type: Mapped[str] = mapped_column(String)
    amount: Mapped[float] = mapped_column(Float)
    date: Mapped[datetime] = mapped_column(DateTime)
