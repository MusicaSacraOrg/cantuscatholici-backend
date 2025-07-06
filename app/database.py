from typing import Annotated

from fastapi import Depends
from sqlmodel import Session, create_engine

from app.config import postgres_settings

engine = create_engine(
    str(postgres_settings.postgres_dsn),
    echo=True,
)


def get_session():
    with Session(engine) as session:
        yield session


DbSessionDep = Annotated[Session, Depends(get_session)]
