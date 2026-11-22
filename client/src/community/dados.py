import sqlite3
from src.storage.db import get_connection  # <-- ajusta para o nome da função em src/storage/db.py


def obter_conexao():
    conn = get_connection()
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


def listar_publicacoes_comunidade(user_id_atual, apenas_outros=True):
    """Lista publicações da comunidade com contagem de likes, dislikes e o voto do utilizador atual."""
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
            ct.type_name,
            COALESCE(SUM(CASE WHEN pv.voto = 1 THEN 1 ELSE 0 END), 0) AS likes,
            COALESCE(SUM(CASE WHEN pv.voto = -1 THEN 1 ELSE 0 END), 0) AS dislikes,
            MAX(CASE WHEN pv.user_id = ? THEN pv.voto ELSE 0 END) AS meu_voto
        FROM publicacao p
        JOIN user u ON p.user_id = u.id
        JOIN captchas c ON p.captcha_id = c.id
        JOIN captchas_type ct ON c.captcha_type_id = ct.id
        LEFT JOIN publicacao_voto pv ON pv.publicacao_id = p.id
    """
    params = [user_id_atual]

    if apenas_outros:
        query += " WHERE p.user_id != ?"
        params.append(user_id_atual)

    query += """
        GROUP BY p.id
        ORDER BY p.created_at DESC
    """

    with obter_conexao() as conn:
        return conn.execute(query, params).fetchall()


def listar_imagens_captcha(captcha_id):
    """Devolve os caminhos das imagens associadas a um captcha."""
    with obter_conexao() as conn:
        return conn.execute(
            "SELECT image_path FROM captchas_image WHERE captcha_id = ?",
            (captcha_id,),
        ).fetchall()


def votar_publicacao(publicacao_id, user_id, voto):
    """
    Regista ou atualiza o voto de um utilizador numa publicação.
    voto: 1 (Like) ou -1 (Dislike)
    """
    if voto not in (1, -1):
        return False

    with obter_conexao() as conn:
        existe = conn.execute(
            "SELECT id FROM publicacao WHERE id = ?",
            (publicacao_id,),
        ).fetchone()
        if not existe:
            return False

        conn.execute(
            """
            INSERT INTO publicacao_voto (publicacao_id, user_id, voto)
            VALUES (?, ?, ?)
            ON CONFLICT(publicacao_id, user_id)
            DO UPDATE SET voto = excluded.voto, created_at = CURRENT_TIMESTAMP
            """,
            (publicacao_id, user_id, voto),
        )
        conn.commit()
        return True


def remover_voto(publicacao_id, user_id):
    """Remove o like/dislike do utilizador numa publicação."""
    with obter_conexao() as conn:
        cursor = conn.execute(
            "DELETE FROM publicacao_voto WHERE publicacao_id = ? AND user_id = ?",
            (publicacao_id, user_id),
        )
        conn.commit()
        return cursor.rowcount > 0


def listar_minhas_publicacoes(user_id):
    """Lista apenas as publicações criadas pelo utilizador autenticado com likes/dislikes."""
    with obter_conexao() as conn:
        return conn.execute(
            """
            SELECT
                p.id AS publicacao_id,
                p.title,
                p.description,
                p.created_at,
                c.name AS captcha_nome,
                c.difficulty,
                COALESCE(SUM(CASE WHEN pv.voto = 1 THEN 1 ELSE 0 END), 0) AS likes,
                COALESCE(SUM(CASE WHEN pv.voto = -1 THEN 1 ELSE 0 END), 0) AS dislikes
            FROM publicacao p
            JOIN captchas c ON p.captcha_id = c.id
            LEFT JOIN publicacao_voto pv ON pv.publicacao_id = p.id
            WHERE p.user_id = ?
            GROUP BY p.id
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