from datetime import datetime
from typing import List

from sqlalchemy import String, DateTime
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import Column
from sqlalchemy import Table
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from database import Base, db


challenge_user_association_table = Table(
    "challenge_user_association_table",
    Base.metadata,
    Column("left_id", ForeignKey("chalenges.id"), primary_key=True),
    Column("right_id", ForeignKey("users.id"), primary_key=True),
)


class ChallengeModel(Base):
    __tablename__ = "chalenges"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String)
    start: Mapped[datetime] = mapped_column(DateTime)
    end: Mapped[datetime] = mapped_column(DateTime)
    prize: Mapped[str] = mapped_column(String)
    users: Mapped[List["UserModel"]] = relationship(
        secondary=challenge_user_association_table, back_populates="chalenges"
    )

    def join(self, user):
        if user not in self.users:
            self.users.append(user)
            db.commit()
