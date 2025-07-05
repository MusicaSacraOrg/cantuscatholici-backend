import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture(scope="session")
def testclient() -> TestClient:
    """Creates and returns test client"""
    return TestClient(app)
