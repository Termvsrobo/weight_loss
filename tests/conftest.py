import pytest

from sqlalchemy_utils import create_database, database_exists, drop_database

from database import Base, db
from models.user import UserModel
from schemas.user import UserSchema


@pytest.fixture(autouse=True, scope="function")
def test_session():
    url = db.bind.engine.url
    if database_exists(url):
        drop_database(url)
    create_database(url)
    Base.metadata.create_all(bind=db.bind)
    yield db
    db.close()


@pytest.fixture(scope="function")
def get_user():
    def _get_user(password, **kwargs):
        new_user = UserSchema(password=password, **kwargs)
        user = UserModel(**{**kwargs, **new_user.model_dump(exclude=['password', 'tariff_status'])})
        user.set_password(password)
        user.create()
        return user
    yield _get_user