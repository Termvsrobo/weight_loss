from datetime import datetime

from sqlalchemy import String, Float, DateTime, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped

from database import Base


class WeightLogModel(Base):
    __tablename__ = "weightlog"
    id: Mapped[int] = mapped_column(primary_key=True)
    date: Mapped[datetime] = mapped_column(DateTime)
    weight: Mapped[float] = mapped_column(Float)
    media_url: Mapped[str] = mapped_column(String, nullable=True, default=None)
    status: Mapped[str] = mapped_column(String)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
