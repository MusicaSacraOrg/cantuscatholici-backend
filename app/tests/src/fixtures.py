import os

import pytest
from dotenv import set_key
from fastapi.testclient import TestClient

import app.config as config
from app.database import Base, SessionLocal, engine
from app.main import app


@pytest.fixture(scope="function")
def testclient(session):  # noqa: ARG001
    """Creates and returns TestClient with lifespan events"""
    with TestClient(app) as client:
        yield client


@pytest.fixture(scope="function", name="session", autouse=True)
def session_fixture():
    """Creates and returns a database session"""
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    with SessionLocal() as db:
        yield db

    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function", name="testenv", autouse=True)
def testenv_fixture(
    tmp_path,
):
    env_file_path = tmp_path / ".env.test"
    env_file_path.touch(mode=0o600, exist_ok=False)

    static_content_prefix = tmp_path / "static_content"
    os.makedirs(static_content_prefix)

    # Change static content prefix to tmp dir
    set_key(
        dotenv_path=env_file_path,
        key_to_set="APP_STATIC_CONTENT_PREFIX",
        value_to_set=str(static_content_prefix),
    )
    # Set database logging to always true
    set_key(
        dotenv_path=env_file_path,
        key_to_set="LOG_DB_ENGINE_ECHO",
        value_to_set="True",
    )

    config.app_settings = config.AppSettings(
        _env_file=env_file_path,  # pyright: ignore [reportCallIssue]
    )
    config.log_settings = config.LogSettings(
        _env_file=env_file_path,  # pyright: ignore [reportCallIssue]
    )

    yield env_file_path

    os.remove(env_file_path)
