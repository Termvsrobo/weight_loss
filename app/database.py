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

    @classmethod
    def update(cls, new_data, **kwargs):
        if kwargs:
            return db.query(cls).filter_by(**kwargs).update(new_data)
        else:
            return db.query(cls)

    def refresh_from_db(self):
        db.refresh(self)

    @classmethod
    def exists(cls, **kwargs):
        if kwargs:
            return db.query(db.query(cls).filter_by(**kwargs).exists()).scalar()
        else:
            return db.query(db.query(cls).exists()).scalar()


def get_db():
    with SessionLocal() as db:
        try:
            yield db
            db.commit()
        except SQLAlchemyError:
            db.rollback()


db = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
