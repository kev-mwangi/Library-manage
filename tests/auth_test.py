import pytest  
import json
import models.auth as auth  


@pytest.fixture
def temp_users_file(tmp_path, monkeypatch):
    test_file = tmp_path / "users.json"
    monkeypatch.setattr(auth, "USERS_FILE", str(test_file))
    auth.current_user = None
    return test_file


def test_register_user(temp_users_file, capsys):
    auth.register_user("john", "password123")

    with open(temp_users_file, "r") as f:
        users = json.load(f)

    assert len(users) == 1
    assert users[0]["username"] == "john"

    captured = capsys.readouterr()
    assert "User registered successfully!" in captured.out


def test_register_duplicate_user(temp_users_file, capsys):
    auth.register_user("john", "password123")
    auth.register_user("john", "password123")

    captured = capsys.readouterr()
    assert "User already exists!" in captured.out


def test_login_success(temp_users_file, capsys):
    auth.register_user("john", "password123")

    result = auth.login("john", "password123")

    assert result is True
    assert auth.current_user["username"] == "john"

    captured = capsys.readouterr()
    assert "Welcome john!" in captured.out


def test_login_failure_wrong_password(temp_users_file, capsys):
    auth.register_user("john", "password123")

    result = auth.login("john", "wrongpass")

    assert result is False
    assert auth.current_user is None

    captured = capsys.readouterr()
    assert "Invalid username or password." in captured.out


def test_login_failure_unknown_user(temp_users_file, capsys):
    result = auth.login("doesnotexist", "password")

    assert result is False

    captured = capsys.readouterr()
    assert "Invalid username or password." in captured.out


def test_logout_when_logged_in(temp_users_file, capsys):
    auth.register_user("john", "password123")
    auth.login("john", "password123")

    auth.logout()

    assert auth.current_user is None

    captured = capsys.readouterr()
    assert "logged out" in captured.out


def test_logout_when_no_user(capsys):
    auth.current_user = None

    auth.logout()

    captured = capsys.readouterr()
    assert "No user is logged in." in captured.out

@pytest.fixture
def temp_users_file(tmp_path, monkeypatch):
    test_file = tmp_path / "users.json"
    monkeypatch.setattr(auth, "USERS_FILE", str(test_file))
    auth.current_user = None

    return test_file


def test_register_user(temp_users_file, capsys):
    auth.register_user("john", "password123")

    with open(temp_users_file, "r") as f:
        users = json.load(f)

    assert len(users) == 1
    assert users[0]["username"] == "john"

    captured = capsys.readouterr()
    assert "User registered successfully!" in captured.out


def test_register_duplicate_user(temp_users_file, capsys):
    auth.register_user("john", "password123")
    auth.register_user("john", "password123")

    captured = capsys.readouterr()
    assert "User already exists!" in captured.out


def test_login_success(temp_users_file, capsys):
    auth.register_user("john", "password123")

    result = auth.login("john", "password123")

    assert result is True
    assert auth.current_user["username"] == "john"

    captured = capsys.readouterr()
    assert "Welcome john!" in captured.out


def test_login_failure_wrong_password(temp_users_file, capsys):
    auth.register_user("john", "password123")

    result = auth.login("john", "wrongpass")

    assert result is False
    assert auth.current_user is None

    captured = capsys.readouterr()
    assert "Invalid username or password." in captured.out


def test_login_failure_unknown_user(temp_users_file, capsys):
    result = auth.login("doesnotexist", "password")

    assert result is False

    captured = capsys.readouterr()
    assert "Invalid username or password." in captured.out


def test_logout_when_logged_in(temp_users_file, capsys):
    auth.register_user("john", "password123")
    auth.login("john", "password123")

    auth.logout()

    assert auth.current_user is None

    captured = capsys.readouterr()
    assert "logged out" in captured.out


def test_logout_when_no_user(capsys):
    auth.current_user = None

    auth.logout()

    captured = capsys.readouterr()
    assert "No user is logged in." in captured.out