import pytest

from src.storage import db
from src.user import accounts, login, passwords


@pytest.fixture(autouse=True)
def fast_hashing(monkeypatch):
    # 600k iterações tornam cada teste lento; o algoritmo é o mesmo
    monkeypatch.setattr(passwords, "ITERATIONS", 1_000)
    login._dummy_hash.cache_clear()


@pytest.fixture
def db_path(tmp_path, monkeypatch):
    path = tmp_path / "test.sqlite"
    db.init_db(path)
    monkeypatch.setattr(accounts, "get_connection", lambda: db.get_connection(path))
    monkeypatch.setattr(login, "get_connection", lambda: db.get_connection(path))
    return path


@pytest.fixture
def answers(monkeypatch):
    """Responde a input() e getpass() pela ordem dada."""

    def feed(*values):
        it = iter(values)
        monkeypatch.setattr("builtins.input", lambda prompt="": next(it))
        monkeypatch.setattr(accounts, "getpass", lambda prompt="": next(it))
        monkeypatch.setattr(login, "getpass", lambda prompt="": next(it))

    return feed
