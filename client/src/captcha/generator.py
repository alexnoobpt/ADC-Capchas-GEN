"""Criação da imagem do CAPTCHA com Pillow."""

from PIL import Image, ImageDraw

from src.config.settings import DEFAULT_TEXT, IMAGE_HEIGHT, IMAGE_WIDTH, TEXT_COLOR, Color
from src.utils.colors import random_color


def generate_captcha(
    text: str = DEFAULT_TEXT,
    width: int = IMAGE_WIDTH,
    height: int = IMAGE_HEIGHT,
    background: Color | None = None,
    text_color: Color = TEXT_COLOR,
) -> Image.Image:
    """Cria uma imagem com o texto centrado.

    Se `background` não for indicado, é escolhida uma cor clara aleatória.
    """
    if background is None:
        background = random_color()

    image = Image.new("RGB", (width, height), background)
    draw = ImageDraw.Draw(image)

    left, top, right, bottom = draw.textbbox((0, 0), text)
    x = (width - (right - left)) / 2 - left
    y = (height - (bottom - top)) / 2 - top

    draw.text((x, y), text, fill=text_color)
    return image
