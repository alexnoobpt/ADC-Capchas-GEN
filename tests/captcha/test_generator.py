import random

from src.captcha import generator
from src.captcha.generator import generate_captcha, generate_text_captcha
from src.config.settings import IMAGE_HEIGHT, IMAGE_WIDTH


def test_default_size_and_mode():
    image = generate_captcha()
    assert image.size == (IMAGE_WIDTH, IMAGE_HEIGHT)
    assert image.mode == "RGB"


def test_custom_background_is_used():
    image = generate_captcha(background=(255, 255, 255))
    assert image.getpixel((0, 0)) == (255, 255, 255)


def test_text_is_drawn():
    image = generate_captcha(background=(255, 255, 255))
    # Se o texto foi desenhado, a imagem tem mais do que uma cor
    assert len(image.getcolors()) > 1


def test_text_captcha_is_the_same_for_the_same_seed():
    a = generate_text_captcha("aB3#kL", random.Random("aB3#kL"))
    b = generate_text_captcha("aB3#kL", random.Random("aB3#kL"))
    assert a.tobytes() == b.tobytes()


def test_text_captcha_grows_for_long_codes():
    assert generate_text_captcha("a" * 18).width > IMAGE_WIDTH


def test_text_captcha_has_strike_lines(monkeypatch):
    com_linhas = generate_text_captcha("abc", random.Random(1))
    monkeypatch.setattr(generator, "STRIKE_LINES", 0)
    sem_linhas = generate_text_captcha("abc", random.Random(1))
    assert com_linhas.tobytes() != sem_linhas.tobytes()
