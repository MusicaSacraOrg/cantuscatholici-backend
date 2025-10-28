import time
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


def test_user_register_returns_refresh_token(testclient):
    """Test that register endpoint returns refreshToken."""
    r = _register_user(
        testclient,
        email="refresh@example.com",
        password="Secret_123")
    assert r.status_code == 200
    data = r.json()
    assert "refreshToken" in data, "refreshToken should be in response"
    assert "accessToken" in data
    assert data.get("tokenType") == "bearer"
    # Verify refresh token has reasonable length
    assert len(data["refreshToken"]) > 20


def test_user_login_returns_refresh_token(testclient):
    """Test that login endpoint returns refreshToken."""
    _register_user(
        testclient,
        email="login@example.com",
        password="Secret_123")
    r = _login(testclient, "login@example.com", "Secret_123")
    assert r.status_code == 200
    data = r.json()
    assert "refreshToken" in data, "refreshToken should be in response"
    assert "accessToken" in data
    assert data.get("tokenType") == "bearer"
    # Verify refresh token has reasonable length
    assert len(data["refreshToken"]) > 20


def test_user_refresh_token_success(testclient):
    """Test that refresh endpoint returns new tokens."""
    # Register to get initial tokens
    r = _register_user(
        testclient,
        email="dave@example.com",
        password="Secret_123")
    assert r.status_code == 200
    initial_data = r.json()
    initial_access_token = initial_data["accessToken"]
    initial_refresh_token = initial_data["refreshToken"]

    # Refresh the token
    # Delay to ensure tokens are created in different seconds
    time.sleep(1)
    refresh_resp = testclient.post(
        "/user/refresh",
        json={"refreshToken": initial_refresh_token},
    )
    assert refresh_resp.status_code == 200
    refresh_data = refresh_resp.json()

    # Verify new tokens are returned
    assert "accessToken" in refresh_data
    assert "refreshToken" in refresh_data
    assert refresh_data["tokenType"] == "bearer"

    # Verify new tokens are different
    assert refresh_data["accessToken"] != initial_access_token
    assert refresh_data["refreshToken"] != initial_refresh_token

    # Verify new access token works
    me = testclient.get(
        "/user",
        headers=_auth_header(
            refresh_data["accessToken"]))
    assert me.status_code == 200
    me_data = me.json()
    assert me_data["email"] == "dave@example.com"


def test_user_refresh_token_rotation_prevents_reuse(testclient):
    """Test that old refresh token cannot be reused (token rotation)."""
    # Register to get initial tokens
    r = _register_user(
        testclient,
        email="eve@example.com",
        password="Secret_123")
    assert r.status_code == 200
    initial_data = r.json()
    initial_refresh_token = initial_data["refreshToken"]

    # First refresh should work
    refresh_resp = testclient.post(
        "/user/refresh",
        json={"refreshToken": initial_refresh_token},
    )
    assert refresh_resp.status_code == 200

    # Second attempt with same refresh token should fail (token rotation)
    duplicate_resp = testclient.post(
        "/user/refresh",
        json={"refreshToken": initial_refresh_token},
    )
    assert duplicate_resp.status_code == 401
    duplicate_data = duplicate_resp.json()
    assert "invalid_refresh_token" in duplicate_data.get("type", "").lower()


def test_user_refresh_token_invalid_token(testclient):
    """Test that invalid refresh token is rejected."""
    r = testclient.post(
        "/user/refresh",
        json={"refreshToken": "invalid_token_123456789"},
    )
    assert r.status_code == 401
    data = r.json()
    assert "invalid_refresh_token" in data.get("type", "").lower()


def test_user_refresh_token_empty_token(testclient):
    """Test that empty refresh token is rejected."""
    r = testclient.post(
        "/user/refresh",
        json={"refreshToken": ""},
    )
    assert r.status_code == 401
