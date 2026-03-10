import re
from enum import StrEnum

from pydantic import (
    PostgresDsn,
    computed_field,
)
from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)


class PostgresSettings(BaseSettings):
    db: str = "cantuscatholici"
    user: str = "cantuscatholici"
    password: str
    host: str
    port: int = 5432

    @computed_field
    def postgres_dsn(self) -> PostgresDsn:
        return PostgresDsn.build(
            scheme="postgresql+psycopg",
            username=self.user,
            password=self.password,
            host=self.host,
            port=self.port,
            path=self.db,
        )

    model_config = SettingsConfigDict(
        env_file=".env",
        secrets_dir="/run/secrets",
        env_prefix="POSTGRES_",
        extra="ignore",
    )


class LogSettings(BaseSettings):
    db_engine_echo: bool = False

    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="LOG_",
        extra="ignore",
    )


class StaticContentFileTypes(StrEnum):
    SVG_FILE = "svg"
    PDF_FILE = "pdf"
    MUSESCORE_FILE = "mscz"
    MP3_FILE = "mp3"


class AppSettings(BaseSettings):
    static_content_prefix: str = "/data/cantuscatholici"

    @computed_field
    @property
    def static_content_db_file_path_regex(self) -> str:
        file_types = [
            re.escape(file_type.value) for file_type in StaticContentFileTypes
        ]
        file_type_regex = r"|".join(file_types)
        return rf"{self.static_content_prefix}/\w*\.(?:{file_type_regex})\.bz"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="APP_",
        extra="ignore",
    )


class AuthSettings(BaseSettings):
    secret_key: str
    algorithm: str = "HS512"
    access_token_expire_minutes: int = 30

    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="AUTH_",
        extra="ignore",
    )


class TranspositionSettings(BaseSettings):
    service_url: str = "http://transposition-service:8001"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="TRANSPOSITION_",
        extra="ignore",
    )


postgres_settings = PostgresSettings()  # pyright: ignore[reportCallIssue]
log_settings = LogSettings()
app_settings = AppSettings()
auth_settings = AuthSettings()  # pyright: ignore[reportCallIssue]
transposition_settings = TranspositionSettings()
