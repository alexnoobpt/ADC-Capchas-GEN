from PIL import Image

from src.captchas import imagem, repositorio


def test_same_captcha_always_gives_the_same_image():
    captcha = {"nome": "a", "desafio": {"codigo": "aB3#kL"}}
    assert imagem.imagem_do_captcha(captcha).tobytes() == imagem.imagem_do_captcha(captcha).tobytes()


def test_menu_without_text_captchas(user_id, capsys):
    repositorio.criar(user_id, "m", "1", "3", {"num1": 1, "operador": "+", "num2": 1}, 2)
    imagem.menu_imagem(user_id)

    assert "Ainda não há CAPTCHAs de texto" in capsys.readouterr().out


def test_menu_shows_image_in_terminal(user_id, answers, monkeypatch):
    shown = []
    monkeypatch.setattr(imagem, "print_image", lambda img: shown.append(img) or True)
    repositorio.criar(user_id, "a", "1", "1", {"codigo": "aB3#kL"}, "aB3#kL")
    answers("a", "1", "3")
    imagem.menu_imagem(user_id)

    assert len(shown) == 1


def test_menu_downloads_png_named_after_captcha(user_id, answers, monkeypatch, tmp_path):
    downloads = tmp_path / "downloads"
    monkeypatch.setattr("src.storage.file_storage.DOWNLOADS_DIR", downloads)
    repositorio.criar(user_id, "meu captcha", "1", "1", {"codigo": "aB3#kL"}, "aB3#kL")
    answers("meu captcha", "2", "3")
    imagem.menu_imagem(user_id)

    [ficheiro] = downloads.iterdir()
    assert ficheiro.name == "meu_captcha.png"
    with Image.open(ficheiro) as img:
        assert img.format == "PNG"


def test_menu_unknown_name(user_id, answers, capsys):
    repositorio.criar(user_id, "a", "1", "1", {"codigo": "aB3#kL"}, "aB3#kL")
    answers("b")
    imagem.menu_imagem(user_id)

    assert "Captcha não encontrado." in capsys.readouterr().out
