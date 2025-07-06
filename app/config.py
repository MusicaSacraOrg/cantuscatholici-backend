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
        extra="allow",
    )


postgres_settings = PostgresSettings()  # pyright: ignore[reportCallIssue]
