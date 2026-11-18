from src.config.settings import IMAGE_HEIGHT, IMAGE_WIDTH
from src.captcha.generator import generate_captcha


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
