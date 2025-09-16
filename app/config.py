from pydantic import PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DB_DSN: PostgresDsn
    model_config = SettingsConfigDict(
        env_file=".env", extra="allow", env_ignore_empty=True, env_parse_none_str=True
    )
