import pytest
from models.user import User   
import hashlib



def test_user_creation_password_is_hashed():
    u = User("john", "password123")
    assert u.password != "password123"
    expected = hashlib.sha256("password123".encode()).hexdigest()
    assert u.password == expected



def test_verify_password_correct():
    u = User("john", "password123")
    assert u.verify_password("password123") is True



def test_verify_password_wrong():
    u = User("john", "password123")
    assert u.verify_password("wrongpass") is False



def test_to_dict_structure():
    u = User("john", "password123", role="admin")
    data = u.to_dict()
    assert data["username"] == "john"
    assert data["role"] == "admin"
    assert "password" in data



def test_default_role():
    u = User("john", "password123")
    assert u.role == "member"