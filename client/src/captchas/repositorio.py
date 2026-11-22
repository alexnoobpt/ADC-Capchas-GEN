"""Guarda e lê os CAPTCHAs de cada utilizador na tabela `captchas`."""
import json
import sqlite3
from contextlib import closing

from src.storage.db import get_connection

NOMES_TIPO = {"1": "Texto", "2": "Emoji", "3": "Matemático"}
TIPO_POR_NOME = {nome: codigo for codigo, nome in NOMES_TIPO.items()}

_SELECT = """
    SELECT c.id, c.name, c.difficulty, t.type_name, c.challenge_data, c.solution
    FROM captchas c JOIN captchas_type t ON t.id = c.captcha_type_id
"""


class NomeRepetido(Exception):
    pass


def _nome_repetido(erro, nome):
    if "UNIQUE" in str(erro):
        raise NomeRepetido(nome) from erro
    raise erro


def _linha(row):
    captcha_id, nome, dificuldade, tipo, desafio, solucao = row
    return {
        "id": captcha_id,
        "nome": nome,
        "dificuldade": dificuldade,
        "tipo": TIPO_POR_NOME[tipo],
        "desafio": json.loads(desafio),
        "solucao": json.loads(solucao),
    }


def _id_do_tipo(conn, tipo):
    return conn.execute("SELECT id FROM captchas_type WHERE type_name = ?", (NOMES_TIPO[tipo],)).fetchone()[0]


def criar(user_id, nome, dificuldade, tipo, desafio, solucao):
    try:
        with closing(get_connection()) as conn, conn:
            cursor = conn.execute(
                "INSERT INTO captchas (user_id, captcha_type_id, name, difficulty, challenge_data, solution) "
                "VALUES (?, ?, ?, ?, ?, ?)",
                (user_id, _id_do_tipo(conn, tipo), nome, dificuldade, json.dumps(desafio), json.dumps(solucao)),
            )
            return cursor.lastrowid
    except sqlite3.IntegrityError as erro:
        _nome_repetido(erro, nome)


def listar(user_id):
    with closing(get_connection()) as conn:
        rows = conn.execute(_SELECT + " WHERE c.user_id = ? ORDER BY c.id", (user_id,)).fetchall()
    return [_linha(row) for row in rows]


def obter(user_id, nome):
    with closing(get_connection()) as conn:
        row = conn.execute(_SELECT + " WHERE c.user_id = ? AND c.name = ?", (user_id, nome)).fetchone()
    return _linha(row) if row else None


def atualizar(captcha):
    try:
        with closing(get_connection()) as conn, conn:
            conn.execute(
                "UPDATE captchas SET name = ?, difficulty = ?, captcha_type_id = ?, challenge_data = ?, solution = ? "
                "WHERE id = ?",
                (
                    captcha["nome"],
                    captcha["dificuldade"],
                    _id_do_tipo(conn, captcha["tipo"]),
                    json.dumps(captcha["desafio"]),
                    json.dumps(captcha["solucao"]),
                    captcha["id"],
                ),
            )
    except sqlite3.IntegrityError as erro:
        _nome_repetido(erro, captcha["nome"])


def eliminar(captcha_id):
    with closing(get_connection()) as conn, conn:
        conn.execute("DELETE FROM captchas WHERE id = ?", (captcha_id,))
