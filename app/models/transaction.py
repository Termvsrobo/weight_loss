from datetime import datetime

from sqlalchemy import String, Float, DateTime
from sqlalchemy.orm import mapped_column, Mapped

from database import Base


class TransactionModel(Base):
    __tablename__ = "transactions"
    id: Mapped[int] = mapped_column(primary_key=True)
    type: Mapped[str] = mapped_column(String)
    amount: Mapped[float] = mapped_column(Float)
    date: Mapped[datetime] = mapped_column(DateTime)
