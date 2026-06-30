import pytest
import requests

from dboss.auth_client import AuthError, get_me, login, register

# --- register ---


def test_register_success(mocker):
    mock_resp = mocker.MagicMock()
    mock_resp.ok = True
    mock_resp.status_code = 201
    mock_resp.json.return_value = {"id": 1, "username": "alice"}
    mocker.patch("dboss.auth_client.requests.post", return_value=mock_resp)

    result = register("alice", "alice@example.com", "secret123")
    assert result["username"] == "alice"


def test_register_duplicate_user(mocker):
    mock_resp = mocker.MagicMock()
    mock_resp.ok = False
    mock_resp.status_code = 400
    mock_resp.json.return_value = {"detail": "Username already exists"}
    mocker.patch("dboss.auth_client.requests.post", return_value=mock_resp)

    with pytest.raises(AuthError, match="Kayıt başarısız"):
        register("alice", "alice@example.com", "secret123")


def test_register_connection_error(mocker):
    mocker.patch(
        "dboss.auth_client.requests.post",
        side_effect=requests.exceptions.ConnectionError,
    )
    with pytest.raises(AuthError, match="bağlanılamadı"):
        register("alice", "alice@example.com", "secret123")


# --- login ---


def test_login_success(mocker):
    mock_resp = mocker.MagicMock()
    mock_resp.ok = True
    mock_resp.status_code = 200
    mock_resp.json.return_value = {"access_token": "tok_abc123"}
    mocker.patch("dboss.auth_client.requests.post", return_value=mock_resp)

    token = login("alice", "secret123")
    assert token == "tok_abc123"


def test_login_wrong_password(mocker):
    mock_resp = mocker.MagicMock()
    mock_resp.ok = False
    mock_resp.status_code = 401
    mocker.patch("dboss.auth_client.requests.post", return_value=mock_resp)

    with pytest.raises(AuthError, match="Kullanıcı adı veya şifre hatalı"):
        login("alice", "wrongpass")


def test_login_connection_error(mocker):
    mocker.patch(
        "dboss.auth_client.requests.post",
        side_effect=requests.exceptions.ConnectionError,
    )
    with pytest.raises(AuthError, match="bağlanılamadı"):
        login("alice", "secret123")


def test_login_missing_token_in_response(mocker):
    mock_resp = mocker.MagicMock()
    mock_resp.ok = True
    mock_resp.status_code = 200
    mock_resp.json.return_value = {}
    mocker.patch("dboss.auth_client.requests.post", return_value=mock_resp)

    with pytest.raises(AuthError, match="geçerli bir token"):
        login("alice", "secret123")


# --- get_me ---


def test_get_me_success(mocker):
    mock_resp = mocker.MagicMock()
    mock_resp.ok = True
    mock_resp.status_code = 200
    mock_resp.json.return_value = {"username": "alice", "email": "alice@example.com"}
    mocker.patch("dboss.auth_client.requests.get", return_value=mock_resp)

    user = get_me("tok_abc123")
    assert user["username"] == "alice"


def test_get_me_expired_token(mocker):
    mock_resp = mocker.MagicMock()
    mock_resp.ok = False
    mock_resp.status_code = 401
    mocker.patch("dboss.auth_client.requests.get", return_value=mock_resp)

    with pytest.raises(AuthError, match="Oturum süresi"):
        get_me("expired_token")


def test_get_me_connection_error(mocker):
    mocker.patch(
        "dboss.auth_client.requests.get",
        side_effect=requests.exceptions.ConnectionError,
    )
    with pytest.raises(AuthError, match="bağlanılamadı"):
        get_me("tok_abc123")
