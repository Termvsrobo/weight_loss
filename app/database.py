from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.exc import IntegrityError

from config import settings

engine = create_engine(settings.DB_DSN.encoded_string())
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    def create(self):
        try:
            db.add(self)
            db.commit()
            return True, ""
        except IntegrityError as e:
            return False, str(e)

    save = create

    @classmethod
    def filter(cls, **kwargs):
        if kwargs:
            return db.query(cls).filter_by(**kwargs)
        else:
            return db.query(cls)


def get_db():
    with SessionLocal() as db:
        try:
            yield db
            db.commit()
        except SQLAlchemyError:
            db.rollback()


db = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
