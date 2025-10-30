from sqlalchemy import Boolean, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped

from database import Base


class PreferenceModel(Base):
    __tablename__ = "preferences"
    id: Mapped[int] = mapped_column(primary_key=True)
    motivation: Mapped[bool] = mapped_column(Boolean, default=False)
    reminders: Mapped[bool] = mapped_column(Boolean, default=False)
    accruals: Mapped[bool] = mapped_column(Boolean, default=False)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
