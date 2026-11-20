import sqlite3
from contextlib import closing

from src.user.accounts import create_account
from src.user.passwords import verify_password


def _users(db_path):
    with closing(sqlite3.connect(db_path)) as conn:
        return conn.execute("SELECT username, email, password_hash FROM user").fetchall()


def test_create_account_saves_hashed_password(db_path, answers, capsys):
    answers("ana", "ana@x.pt", "segredo1")
    create_account()

    [(username, email, password_hash)] = _users(db_path)
    assert (username, email) == ("ana", "ana@x.pt")
    assert password_hash != "segredo1"
    assert verify_password("segredo1", password_hash)
    assert "Account created successfully!" in capsys.readouterr().out


def test_username_and_email_are_normalized(db_path, answers):
    answers("  ana ", " Ana@X.pt ", "segredo1")
    create_account()

    [(username, email, _)] = _users(db_path)
    assert (username, email) == ("ana", "ana@x.pt")


def test_empty_username_and_invalid_email_are_asked_again(db_path, answers):
    answers("   ", "ana", "ana@", "ana@x", "ana@x.pt", "segredo1")
    create_account()

    [(username, email, _)] = _users(db_path)
    assert (username, email) == ("ana", "ana@x.pt")


def test_short_password_is_asked_again(db_path, answers):
    answers("ana", "ana@x.pt", "123", "segredo1")
    create_account()

    [(_, _, password_hash)] = _users(db_path)
    assert verify_password("segredo1", password_hash)


def test_duplicate_username_is_rejected(db_path, answers, capsys):
    answers("ana", "ana@x.pt", "segredo1")
    create_account()
    answers("ana", "outra@x.pt", "segredo2")
    create_account()

    assert len(_users(db_path)) == 1
    assert "Username or email already exists." in capsys.readouterr().out
