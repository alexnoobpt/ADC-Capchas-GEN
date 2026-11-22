Python

import sqlite3

DB_PATH = "base_dados.db"  # Altera para o nome/caminho da tua BD


def obter_conexao():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


def listar_captchas_do_utilizador(user_id):
    """Devolve os captchas criados pelo utilizador que podem ser publicados."""
    with obter_conexao() as conn:
        return conn.execute(
            """
            SELECT c.id, c.name, c.difficulty, ct.type_name
            FROM captchas c
            JOIN captchas_type ct ON c.captcha_type_id = ct.id
            WHERE c.user_id = ?
            ORDER BY c.created_at DESC
            """,
            (user_id,),
        ).fetchall()


def criar_publicacao(user_id, captcha_id, title, description):
    """Publica um captcha na comunidade (valida que o captcha pertence ao utilizador)."""
    with obter_conexao() as conn:
        dono = conn.execute(
            "SELECT id FROM captchas WHERE id = ? AND user_id = ?",
            (captcha_id, user_id),
        ).fetchone()
        if not dono:
            return False

        conn.execute(
            """
            INSERT INTO publicacao (user_id, captcha_id, title, description)
            VALUES (?, ?, ?, ?)
            """,
            (user_id, captcha_id, title, description),
        )
        conn.commit()
        return True


def listar_publicacoes_comunidade(excluir_user_id=None):
    """Lista publicações da comunidade com dados do autor e do captcha."""
    query = """
        SELECT
            p.id AS publicacao_id,
            p.title,
            p.description,
            p.created_at,
            u.username AS autor,
            c.id AS captcha_id,
            c.name AS captcha_nome,
            c.difficulty,
            c.challenge_data,
            c.solution,
            ct.type_name
        FROM publicacao p
        JOIN user u ON p.user_id = u.id
        JOIN captchas c ON p.captcha_id = c.id
        JOIN captchas_type ct ON c.captcha_type_id = ct.id
    """
    params = []
    if excluir_user_id is not None:
        query += " WHERE p.user_id != ?"
        params.append(excluir_user_id)

    query += " ORDER BY p.created_at DESC"

    with obter_conexao() as conn:
        return conn.execute(query, params).fetchall()


def listar_imagens_captcha(captcha_id):
    """Devolve os caminhos das imagens associadas a um captcha."""
    with obter_conexao() as conn:
        return conn.execute(
            "SELECT image_path FROM captchas_image WHERE captcha_id = ?",
            (captcha_id,),
        ).fetchall()


def listar_minhas_publicacoes(user_id):
    """Lista apenas as publicações criadas pelo utilizador autenticado."""
    with obter_conexao() as conn:
        return conn.execute(
            """
            SELECT
                p.id AS publicacao_id,
                p.title,
                p.description,
                p.created_at,
                c.name AS captcha_nome,
                c.difficulty
            FROM publicacao p
            JOIN captchas c ON p.captcha_id = c.id
            WHERE p.user_id = ?
            ORDER BY p.created_at DESC
            """,
            (user_id,),
        ).fetchall()


def atualizar_publicacao(publicacao_id, user_id, novo_titulo, nova_descricao):
    """Edita o título e a descrição de uma publicação do utilizador."""
    with obter_conexao() as conn:
        cursor = conn.execute(
            """
            UPDATE publicacao
            SET title = ?, description = ?
            WHERE id = ? AND user_id = ?
            """,
            (novo_titulo, nova_descricao, publicacao_id, user_id),
        )
        conn.commit()
        return cursor.rowcount > 0


def eliminar_publicacao(publicacao_id, user_id):
    """Retira uma publicação da comunidade (não apaga o captcha da tabela captchas)."""
    with obter_conexao() as conn:
        cursor = conn.execute(
            "DELETE FROM publicacao WHERE id = ? AND user_id = ?",
            (publicacao_id, user_id),
        )
        conn.commit()
        return cursor.rowcount > 0