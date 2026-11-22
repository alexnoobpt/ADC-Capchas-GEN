import sqlite3
from contextlib import closing

import pytest

from src.captchas import repositorio
from src.captchas.repositorio import NomeRepetido
from src.storage import db


@pytest.fixture
def users(tmp_path, monkeypatch):
    path = tmp_path / "test.sqlite"
    db.init_db(path)
    monkeypatch.setattr(repositorio, "get_connection", lambda: db.get_connection(path))
    with closing(db.get_connection(path)) as conn, conn:
        for nome in ("ana", "rui"):
            conn.execute("INSERT INTO user (username, email, password_hash) VALUES (?, ?, 'h')", (nome, f"{nome}@x.pt"))
    return 1, 2


def test_create_and_read_back(users):
    ana, _ = users
    repositorio.criar(ana, "a", "2", "3", {"num1": 1, "operador": "+", "num2": 2}, 3)

    [captcha] = repositorio.listar(ana)
    assert captcha["nome"] == "a"
    assert captcha["dificuldade"] == "2"
    assert captcha["tipo"] == "3"
    assert captcha["desafio"] == {"num1": 1, "operador": "+", "num2": 2}
    assert captcha["solucao"] == 3


def test_emoji_solution_round_trips(users):
    ana, _ = users
    repositorio.criar(ana, "e", "1", "2", {"categoria": "Animais", "quantidade": 1, "opcoes": ["🐺"]}, ["🐺"])

    assert repositorio.obter(ana, "e")["solucao"] == ["🐺"]


def test_each_user_only_sees_their_captchas(users):
    ana, rui = users
    repositorio.criar(ana, "a", "1", "1", {"codigo": "x"}, "x")

    assert repositorio.listar(rui) == []
    assert repositorio.obter(rui, "a") is None


def test_same_name_is_rejected_for_the_same_user_only(users):
    ana, rui = users
    repositorio.criar(ana, "a", "1", "1", {"codigo": "x"}, "x")

    with pytest.raises(NomeRepetido):
        repositorio.criar(ana, "a", "1", "1", {"codigo": "y"}, "y")
    repositorio.criar(rui, "a", "1", "1", {"codigo": "y"}, "y")


def test_unknown_user_is_not_a_repeated_name(users):
    with pytest.raises(sqlite3.IntegrityError):
        repositorio.criar(999, "a", "1", "1", {"codigo": "x"}, "x")


def test_update(users):
    ana, _ = users
    repositorio.criar(ana, "a", "1", "1", {"codigo": "x"}, "x")
    captcha = repositorio.obter(ana, "a")
    captcha.update(nome="b", tipo="3", desafio={"num1": 1, "operador": "+", "num2": 1}, solucao=2)
    repositorio.atualizar(captcha)

    assert repositorio.obter(ana, "a") is None
    assert repositorio.obter(ana, "b")["tipo"] == "3"


def test_update_to_a_repeated_name(users):
    ana, _ = users
    repositorio.criar(ana, "a", "1", "1", {"codigo": "x"}, "x")
    repositorio.criar(ana, "b", "1", "1", {"codigo": "y"}, "y")
    captcha = repositorio.obter(ana, "b")
    captcha["nome"] = "a"

    with pytest.raises(NomeRepetido):
        repositorio.atualizar(captcha)


def test_delete(users):
    ana, _ = users
    repositorio.criar(ana, "a", "1", "1", {"codigo": "x"}, "x")
    repositorio.eliminar(repositorio.obter(ana, "a")["id"])

    assert repositorio.listar(ana) == []
