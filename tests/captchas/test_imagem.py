import pytest
from PIL import Image

from src.captchas import criar, dados, editar, imagem
from src.captchas.criar import SIMBOLOS, TAMANHO_CODIGO


@pytest.fixture(autouse=True)
def lista_vazia():
    dados.captchas.clear()
    yield
    dados.captchas.clear()


@pytest.fixture
def answers(monkeypatch):
    def feed(*values):
        it = iter(values)
        monkeypatch.setattr("builtins.input", lambda prompt="": next(it))

    return feed


def test_text_captcha_keeps_its_code(answers):
    answers("a", "2", "1", "0")
    criar.criar_captcha()

    [(nome, dificuldade, tipo, codigo)] = dados.captchas
    assert (nome, dificuldade, tipo) == ("a", "2", "1")
    assert len(codigo) == TAMANHO_CODIGO["2"]
    assert not set(codigo) & set("£§")


def test_math_captcha_has_no_code(answers):
    answers("m", "1", "3", "0")
    criar.criar_captcha()

    assert dados.captchas[0][3] is None


def test_symbols_question_counts_the_same_symbols(answers, monkeypatch, capsys):
    monkeypatch.setattr(criar, "gerar_codigo_texto", lambda dificuldade: "ab!#C1")
    monkeypatch.setattr(criar.random, "choice", lambda perguntas: perguntas[-1])
    answers("s", "1", "1", "2")
    criar.criar_captcha()

    assert set("!#") <= set(SIMBOLOS)
    assert "Resposta correta!" in capsys.readouterr().out


def test_editing_difficulty_generates_a_new_code(answers):
    dados.captchas.append(["a", "1", "1", "abcdef"])
    answers("a", "2", "3")
    editar.editar_captcha()

    assert len(dados.captchas[0][3]) == TAMANHO_CODIGO["3"]


def test_editing_only_the_name_keeps_the_code(answers):
    dados.captchas.append(["a", "1", "1", "abcdef"])
    answers("a", "1", "b")
    editar.editar_captcha()

    assert dados.captchas[0] == ["b", "1", "1", "abcdef"]


def test_changing_to_math_removes_the_code(answers):
    dados.captchas.append(["a", "1", "1", "abcdef"])
    answers("a", "3", "3")
    editar.editar_captcha()

    assert dados.captchas[0][3] is None


def test_same_captcha_always_gives_the_same_image():
    captcha = ["a", "1", "1", "aB3#kL"]
    assert imagem.imagem_do_captcha(captcha).tobytes() == imagem.imagem_do_captcha(captcha).tobytes()


def test_menu_without_text_captchas(answers, capsys):
    dados.captchas.append(["m", "1", "3", None])
    imagem.menu_imagem()

    assert "Ainda não há CAPTCHAs de texto" in capsys.readouterr().out


def test_menu_shows_image_in_terminal(answers, monkeypatch):
    shown = []
    monkeypatch.setattr(imagem, "print_image", lambda img: shown.append(img) or True)
    dados.captchas.append(["a", "1", "1", "aB3#kL"])
    answers("a", "1", "3")
    imagem.menu_imagem()

    assert len(shown) == 1


def test_menu_downloads_png_named_after_captcha(answers, monkeypatch, tmp_path):
    monkeypatch.setattr("src.storage.file_storage.DOWNLOADS_DIR", tmp_path)
    dados.captchas.append(["meu captcha", "1", "1", "aB3#kL"])
    answers("meu captcha", "2", "3")
    imagem.menu_imagem()

    [ficheiro] = tmp_path.iterdir()
    assert ficheiro.name == "meu_captcha.png"
    with Image.open(ficheiro) as img:
        assert img.format == "PNG"


def test_menu_unknown_name(answers, capsys):
    dados.captchas.append(["a", "1", "1", "aB3#kL"])
    answers("b")
    imagem.menu_imagem()

    assert "Captcha não encontrado." in capsys.readouterr().out
