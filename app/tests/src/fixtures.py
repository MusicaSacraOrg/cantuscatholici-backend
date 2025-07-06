import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session

from app.database import engine
from app.main import app


@pytest.fixture(scope="session")
def testclient() -> TestClient:
    """Creates and returns test client"""
    return TestClient(app)


@pytest.fixture(scope="function", name="session")
def session_fixture():
    """Creates and returns a database session"""
    with Session(engine) as session:
        yield session
