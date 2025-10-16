from sqlalchemy import String
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import Integer

from database import Base


class TariffModel(Base):
    __tablename__ = "tariffs"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String)
    percent: Mapped[int] = mapped_column(Integer)
    description: Mapped[str] = mapped_column(String, nullable=True, default=None)
