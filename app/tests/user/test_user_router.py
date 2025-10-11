from logging import getLogger

from starlette import status

global_logger = getLogger(__name__)


def _register_user(
    client,
    email="alice@example.com",
    password="Secret_123",
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
    assert me_data["mobile"] == "tel:+1-415-555-2671"
    assert "id" in me_data


def test_user_login_success_after_register(testclient):
    _register_user(testclient, email="bob@example.com", password="Pw_123456")
    r = _login(testclient, "bob@example.com", "Pw_123456")
    assert r.status_code == 200
    j = r.json()
    assert "accessToken" in j and j.get("tokenType") == "bearer"


def test_user_login_wrong_password(testclient):
    _register_user(testclient, email="carol@example.com", password="Right_pw1")
    r = _login(testclient, "carol@example.com", "wrongpw")
    assert r.status_code == 401  # invalid credentials


def test_user_register_duplicate_email(testclient):
    first = _register_user(testclient, email="dup@example.com")
    assert first.status_code == 200

    second = _register_user(testclient, email="dup@example.com")
    assert second.status_code == status.HTTP_409_CONFLICT
    second = second.json()
    assert second["type"] == "https://cantuscatholici.sk/probs/email_taken"
    assert second["detail"] == "Email already in use"


def test_user_register_invalid_email_rejected(testclient):
    r = _register_user(testclient, email="not-an-email")
    assert r.status_code == 422, (
        f"Expected 422 for invalid email, got {r.status_code}: {r.text}"
    )


def test_user_register_invalid_password_rejected(testclient):
    r = _register_user(testclient, email="alice@example.com", password="weak")
    assert r.status_code == 422, (
        f"Expected 422 for invalid password, got {r.status_code}: {r.text}"
    )
