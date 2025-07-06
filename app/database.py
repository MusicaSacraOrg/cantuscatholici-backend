from typing import Annotated

from fastapi import Depends
from sqlmodel import Session, create_engine

from app.config import log_settings, postgres_settings

engine = create_engine(
    str(postgres_settings.postgres_dsn),
    echo=log_settings.db_engine_echo,
)


def get_session():
    with Session(engine) as session:
        yield session


DbSessionDep = Annotated[Session, Depends(get_session)]
