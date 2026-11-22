from src.captchas import repositorio
from src.captchas.consultar import ver_captchas
from src.captchas.criar import criar_captcha
from src.captchas.desafios import TAMANHO_CODIGO
from src.captchas.editar import editar_captcha
from src.captchas.eliminar import eliminar_captcha


def test_created_captcha_is_saved(user_id, answers):
    answers("a", "2", "3", "0")
    criar_captcha(user_id)

    [captcha] = repositorio.listar(user_id)
    assert (captcha["nome"], captcha["dificuldade"], captcha["tipo"]) == ("a", "2", "3")
    assert set(captcha["desafio"]) == {"num1", "operador", "num2"}


def test_saved_captcha_survives_a_new_session(user_id, answers):
    answers("a", "1", "1", "0")
    criar_captcha(user_id)

    # Nova leitura da base de dados, como depois de reiniciar a aplicação
    assert repositorio.obter(user_id, "a")["desafio"]["codigo"]


def test_repeated_name_is_rejected(user_id, answers, capsys):
    repositorio.criar(user_id, "a", "1", "1", {"codigo": "x"}, "x")
    answers("a")
    criar_captcha(user_id)

    assert "Esse nome já se encontra registrado!" in capsys.readouterr().out
    assert len(repositorio.listar(user_id)) == 1


def test_list_groups_by_difficulty(user_id, capsys):
    repositorio.criar(user_id, "dificil", "3", "1", {"codigo": "x"}, "x")
    repositorio.criar(user_id, "facil", "1", "3", {"num1": 1, "operador": "+", "num2": 1}, 2)
    ver_captchas(user_id)

    out = capsys.readouterr().out
    assert out.index("--- Fácil ---") < out.index("Nome: facil, Tipo: Matemático")
    assert out.index("--- Difícil ---") < out.index("Nome: dificil, Tipo: Texto")


def test_editing_only_the_name_keeps_the_challenge(user_id, answers):
    repositorio.criar(user_id, "a", "1", "1", {"codigo": "abcdef"}, "abcdef")
    answers("a", "1", "b")
    editar_captcha(user_id)

    captcha = repositorio.obter(user_id, "b")
    assert captcha["desafio"] == {"codigo": "abcdef"}


def test_editing_difficulty_generates_a_new_challenge(user_id, answers):
    repositorio.criar(user_id, "a", "1", "1", {"codigo": "abcdef"}, "abcdef")
    answers("a", "2", "3")
    editar_captcha(user_id)

    assert len(repositorio.obter(user_id, "a")["desafio"]["codigo"]) == TAMANHO_CODIGO["3"]


def test_editing_type_to_math(user_id, answers):
    repositorio.criar(user_id, "a", "1", "1", {"codigo": "abcdef"}, "abcdef")
    answers("a", "3", "3")
    editar_captcha(user_id)

    captcha = repositorio.obter(user_id, "a")
    assert captcha["tipo"] == "3"
    assert "num1" in captcha["desafio"]


def test_editing_to_a_repeated_name(user_id, answers, capsys):
    repositorio.criar(user_id, "a", "1", "1", {"codigo": "x"}, "x")
    repositorio.criar(user_id, "b", "1", "1", {"codigo": "y"}, "y")
    answers("b", "1", "a")
    editar_captcha(user_id)

    assert "Esse nome já se encontra registrado!" in capsys.readouterr().out
    assert repositorio.obter(user_id, "b") is not None


def test_delete_after_confirmation(user_id, answers):
    repositorio.criar(user_id, "a", "1", "1", {"codigo": "x"}, "x")
    answers("a", "s")
    eliminar_captcha(user_id)

    assert repositorio.listar(user_id) == []


def test_delete_cancelled(user_id, answers):
    repositorio.criar(user_id, "a", "1", "1", {"codigo": "x"}, "x")
    answers("a", "n")
    eliminar_captcha(user_id)

    assert len(repositorio.listar(user_id)) == 1
