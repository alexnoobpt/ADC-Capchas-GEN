from src.user import login, passwords
from src.user.accounts import create_account
from src.user.login import log_in


def _register(answers, username="ana", password="segredo1"):
    answers(username, f"{username}@x.pt", password)
    create_account()


def test_login_with_correct_password_returns_session(db_path, answers):
    _register(answers)
    answers("ana", "segredo1")

    session = log_in()

    assert session["username"] == "ana"
    assert session["logged_in"] is True


def test_login_ignores_spaces_around_username(db_path, answers):
    _register(answers)
    answers(" ana ", "segredo1")

    assert log_in() is not None


def test_login_with_wrong_password_fails(db_path, answers, capsys):
    _register(answers)
    answers("ana", "errada")

    assert log_in() is None
    assert "Invalid username or password." in capsys.readouterr().out


def test_unknown_user_still_runs_password_check(db_path, answers, monkeypatch):
    calls = []
    real_verify = passwords.verify_password
    monkeypatch.setattr(login, "verify_password", lambda *a: calls.append(a) or real_verify(*a))
    answers("ninguem", "segredo1")

    assert log_in() is None
    assert len(calls) == 1
