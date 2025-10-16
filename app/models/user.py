from typing import List

import bcrypt
from sqlalchemy import String, Float, Boolean, ForeignKey
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy.orm import relationship

from database import Base, db


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

    @classmethod
    def update(cls, new_data, **kwargs):
        if kwargs:
            return db.query(UserModel).filter_by(**kwargs).update(new_data)
        else:
            return db.query(UserModel)

    def top_up(self, amount: float):
        if self.deposit is None:
            self.deposit = amount
        else:
            self.deposit += amount
        self.save()

    def refresh_from_db(self):
        db.refresh(self)
