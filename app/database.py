from typing import Annotated

from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, declarative_base, sessionmaker

from app.config import log_settings, postgres_settings

engine = create_engine(
    str(postgres_settings.postgres_dsn),
    echo=log_settings.db_engine_echo,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

DbSessionDep = Annotated[Session, Depends(get_session)]
