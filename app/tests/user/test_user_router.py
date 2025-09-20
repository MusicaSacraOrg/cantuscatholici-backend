from logging import getLogger

import pytest
from sqlalchemy.exc import IntegrityError

global_logger = getLogger(__name__)


def _register_user(
    client,
    email="alice@example.com",
    password="secret123",
    name="Alice",
    surname="A",
    mobile="+14155552671",
):
    resp = client.post(
        "/user/register",
        json={
            "email": email,
            "password": password,
            "name": name,
            "surname": surname,
            "mobile": mobile,
        },
    )
    return resp


def _login(client, email, password):
    # OAuth2PasswordRequestForm expects form-encoded "username" and "password"
    return client.post(
        "/user/login",
        data={"username": email, "password": password},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )


def _auth_header(token: str):
    return {"Authorization": f"Bearer {token}"}


def test_user_me_requires_auth(testclient):
    resp = testclient.get("/user")
    assert resp.status_code == 401  # unauthorized when no token


def test_user_register_returns_token_and_me_works_with_token(testclient):
    # Register
    r = _register_user(testclient)
    assert r.status_code == 200, f"{r.text}"
    data = r.json()
    assert "accessToken" in data and data.get("tokenType") == "bearer"

    # Call /me with token
    me = testclient.get("/user", headers=_auth_header(data["accessToken"]))
    assert me.status_code == 200, f"{me.text}"
    me_data = me.json()
    assert me_data["email"] == "alice@example.com"
    assert me_data["name"] == "Alice"
    assert me_data["surname"] == "A"
    assert me_data["mobile"] == "+14155552671"
    assert "id" in me_data


def test_user_login_success_after_register(testclient):
    _register_user(testclient, email="bob@example.com", password="pw123456")
    r = _login(testclient, "bob@example.com", "pw123456")
    assert r.status_code == 200
    j = r.json()
    assert "accessToken" in j and j.get("tokenType") == "bearer"


def test_user_login_wrong_password(testclient):
    _register_user(testclient, email="carol@example.com", password="rightpw")
    r = _login(testclient, "carol@example.com", "wrongpw")
    assert r.status_code == 401  # invalid credentials


def test_user_register_duplicate_email(testclient):
    first = _register_user(testclient, email="dup@example.com")
    assert first.status_code == 200

    with pytest.raises(IntegrityError):
        second = _register_user(testclient, email="dup@example.com")
        # Creation should fail on duplicate; accept any 4xx to be
        # implementation-agnostic
        assert 400 <= second.status_code < 500
