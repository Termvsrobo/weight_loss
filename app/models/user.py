from typing import List

import bcrypt
from sqlalchemy import Boolean, Float, ForeignKey, String, event
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


class UserModel(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    password_hash: Mapped[str] = mapped_column(String(128))
    phone: Mapped[str] = mapped_column(String, unique=True)
    name: Mapped[str] = mapped_column(String, nullable=True, default=None)
    email: Mapped[str] = mapped_column(String, nullable=True, default=None)
    country: Mapped[str] = mapped_column(String, nullable=True, default=None)
    telegram: Mapped[str] = mapped_column(String, nullable=True, default=None)
    avatar_url: Mapped[str] = mapped_column(String, nullable=True, default=None)
    tariff_id: Mapped[int] = mapped_column(
        ForeignKey("tariffs.id"), nullable=True, default=None
    )
    tariff: Mapped["TariffModel"] = relationship()
    deposit: Mapped[float] = mapped_column(Float, nullable=True, default=None)
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False)
    chalenges: Mapped[List["ChallengeModel"]] = relationship(
        secondary="challenge_user_association_table", back_populates="users"
    )

    @hybrid_property
    def tariff_status(self):
        if self.tariff:
            return self.tariff.name
        return None

    def set_password(self, password):
        pw = password.encode("utf-8")
        s = bcrypt.gensalt()
        self.password_hash = bcrypt.hashpw(pw, s).decode("utf-8")
        self.save()

    def check_password(self, password):
        entered_pw = password.encode("utf-8")
        return bcrypt.checkpw(entered_pw, self.password_hash.encode("utf-8"))

    def top_up(self, amount: float):
        if self.deposit is None:
            self.deposit = amount
        else:
            self.deposit += amount
        self.save()


@event.listens_for(UserModel, "after_insert")
def add_tariff_to_user(mapper, connection, target):
    tariff_model = next(
        filter(lambda x: x.class_.__name__ == "TariffModel", mapper.registry.mappers)
    )
    tariff = tariff_model.class_.filter(name="Стартовый").one()
    if tariff:
        target.__class__.update({"tariff_id": tariff.id}, id=target.id)
