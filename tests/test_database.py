# tests/test_database.py

import pytest
from app.database import Database

@pytest.fixture
def db():
    db = Database()
    db.connect()
    yield db
    db.disconnect()

def test_add_user_success(db):
    result = db.add_user("alice", "alice@example.com")
    assert result is True

def test_add_user_duplicate(db):
    db.add_user("bob", "bob@example.com")
    result = db.add_user("bob", "bob@example.com")
    assert result is False  # utilisateur déjà existant

def test_get_user_found(db):
    db.add_user("charlie", "charlie@example.com")
    user = db.get_user("charlie")
    assert user is not None
    assert user["username"] == "charlie"
    assert user["email"] == "charlie@example.com"

def test_get_user_not_found(db):
    user = db.get_user("nobody")
    assert user is None

def test_delete_user_success(db):
    db.add_user("david", "david@example.com")
    result = db.delete_user("david")
    assert result is True
    assert db.get_user("david") is None

def test_delete_user_not_found(db):
    result = db.delete_user("ghost")
    assert result is False
