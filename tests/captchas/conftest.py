from contextlib import closing

import pytest

from src.captchas import repositorio
from src.storage import db


@pytest.fixture
def user_id(tmp_path, monkeypatch):
    path = tmp_path / "test.sqlite"
    db.init_db(path)
    monkeypatch.setattr(repositorio, "get_connection", lambda: db.get_connection(path))
    with closing(db.get_connection(path)) as conn, conn:
        conn.execute("INSERT INTO user (username, email, password_hash) VALUES ('ana', 'ana@x.pt', 'h')")
    return 1


@pytest.fixture
def answers(monkeypatch):
    def feed(*values):
        it = iter(values)
        monkeypatch.setattr("builtins.input", lambda prompt="": next(it))

    return feed
