import logging

from fastapi import status
from fastapi.testclient import TestClient

global_logger = logging.getLogger(__name__)


def test_user_roles_get(
    testclient: TestClient,
):
    # Context manager must be used to run lifespan events, i.e.
    # ensuring predefined user roles exist
    with testclient:
        response = testclient.get(
            "/user_role",
        )

    expected = {
        "limit": 10,
        "offset": 0,
        "total": 3,
        "items": [
            {
                "id": 1,
                "role": "Admin",
            },
            {
                "id": 2,
                "role": "Redactor",
            },
            {
                "id": 3,
                "role": "User",
            },
        ],
    }
    global_logger.warning(f"{response.json()=}")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == expected
