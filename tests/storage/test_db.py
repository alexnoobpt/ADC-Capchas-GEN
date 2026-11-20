import sqlite3
from contextlib import closing

import pytest

from src.storage.db import get_connection, init_db


@pytest.fixture
def db_path(tmp_path):
    path = tmp_path / "test.sqlite"
    init_db(path)
    return path


def test_init_db_creates_tables(db_path):
    with closing(get_connection(db_path)) as conn:
        tables = {row[0] for row in conn.execute("SELECT name FROM sqlite_master WHERE type='table'")}
    assert {"user", "captchas_type", "captchas", "captchas_image", "publicacao"} <= tables


def test_init_db_can_run_twice(db_path):
    init_db(db_path)


def test_init_db_releases_the_file(db_path):
    # Se a ligação ficasse aberta, no Windows o ficheiro não podia ser apagado
    db_path.unlink()
    assert not db_path.exists()


def test_foreign_keys_are_enforced(db_path):
    with closing(get_connection(db_path)) as conn, pytest.raises(sqlite3.IntegrityError):
        conn.execute(
            "INSERT INTO captchas (user_id, captcha_type_id, name, difficulty, solution) "
            "VALUES (999, 999, 'n', '1', 's')"
        )


def test_deleting_user_cascades_to_captchas(db_path):
    with closing(get_connection(db_path)) as conn, conn:
        conn.execute("INSERT INTO user (username, email, password_hash) VALUES ('ana', 'ana@x.pt', 'h')")
        conn.execute("INSERT INTO captchas_type (type_name) VALUES ('texto')")
        conn.execute(
            "INSERT INTO captchas (user_id, captcha_type_id, name, difficulty, solution) "
            "VALUES (1, 1, 'n', '1', 's')"
        )
        conn.execute("DELETE FROM user WHERE id = 1")
        assert conn.execute("SELECT COUNT(*) FROM captchas").fetchone()[0] == 0


def test_update_refreshes_changed_at(db_path):
    with closing(get_connection(db_path)) as conn, conn:
        conn.execute("INSERT INTO user (username, email, password_hash) VALUES ('ana', 'ana@x.pt', 'h')")
        conn.execute("INSERT INTO captchas_type (type_name) VALUES ('texto')")
        conn.execute(
            "INSERT INTO captchas (user_id, captcha_type_id, name, difficulty, solution, changed_at) "
            "VALUES (1, 1, 'n', '1', 's', '2000-01-01 00:00:00')"
        )
        conn.execute("UPDATE captchas SET name = 'outro' WHERE id = 1")
        changed_at = conn.execute("SELECT changed_at FROM captchas WHERE id = 1").fetchone()[0]
    assert changed_at != "2000-01-01 00:00:00"
