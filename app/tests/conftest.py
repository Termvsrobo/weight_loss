from argparse import Namespace
from typing import Optional, Union
from pathlib import Path

import pytest

from alembic.command import upgrade
from alembic.config import Config as AlembicConfig
from sqlalchemy_utils import create_database, database_exists, drop_database

from config import settings
from database import db
from models.user import UserModel
from schemas.user import UserSchema


def make_alembic_config(
    cmd_opts: Namespace, base_path: Union[str, Path] = Path(__file__).parent.parent
) -> AlembicConfig:
    # Replace path to alembic.ini file to absolute
    base_path = Path(base_path)
    if not Path(cmd_opts.config).is_absolute():
        cmd_opts.config = str(base_path.joinpath(cmd_opts.config).absolute())
    config = AlembicConfig(
        file_=cmd_opts.config,
        ini_section=cmd_opts.name,
        cmd_opts=cmd_opts,
    )
    # Replace path to alembic folder to absolute
    alembic_location = config.get_main_option("script_location")
    if not Path(alembic_location).is_absolute():
        config.set_main_option(
            "script_location", str(base_path.joinpath(alembic_location).absolute())
        )
    if cmd_opts.pg_url:
        config.set_main_option("sqlalchemy.url", cmd_opts.pg_url)
    return config


def alembic_config_from_url(pg_url: Optional[str] = None) -> AlembicConfig:
    """Provides python object, representing alembic.ini file."""
    cmd_options = Namespace(
        config="alembic.ini",  # Config file name
        name="alembic",  # Name of section in .ini file to use for Alembic config
        pg_url=pg_url,  # DB URI
        raiseerr=True,  # Raise a full stack trace on error
        x=None,  # Additional arguments consumed by custom env.py scripts
    )
    return make_alembic_config(cmd_opts=cmd_options)


@pytest.fixture(autouse=True, scope="function")
def test_session():
    url = db.bind.engine.url
    if database_exists(url):
        drop_database(url)
    create_database(url)
    alembic_config = alembic_config_from_url(settings.DB_DSN.encoded_string())
    upgrade(alembic_config, "head")
    yield db
    db.close()


@pytest.fixture(scope="function")
def get_user():
    def _get_user(password, **kwargs):
        new_user = UserSchema(password=password, **kwargs)
        user = UserModel(
            **{**kwargs, **new_user.model_dump(exclude=["password", "tariff_status"])}
        )
        user.set_password(password)
        user.create()
        return user

    yield _get_user
