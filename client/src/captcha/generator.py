"""Criação da imagem do CAPTCHA com Pillow."""

import random

from PIL import Image, ImageDraw, ImageFont

from src.config.settings import (
    CAPTCHA_FONT_SIZE,
    DEFAULT_TEXT,
    IMAGE_HEIGHT,
    IMAGE_PADDING,
    IMAGE_WIDTH,
    STRIKE_LINES,
    TEXT_COLOR,
    Color,
)
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


def generate_text_captcha(code: str, rng: random.Random | None = None) -> Image.Image:
    """Cria a imagem de um CAPTCHA de texto: o código em letra grande, riscado por traços aleatórios.

    Com o mesmo `rng` (ex.: `random.Random(code)`) a imagem sai sempre igual.
    """
    rng = rng or random.Random()
    font = ImageFont.load_default(size=CAPTCHA_FONT_SIZE)

    left, top, right, bottom = ImageDraw.Draw(Image.new("RGB", (1, 1))).textbbox((0, 0), code, font=font)
    width = max(IMAGE_WIDTH, right - left + 2 * IMAGE_PADDING)
    height = max(IMAGE_HEIGHT, bottom - top + 2 * IMAGE_PADDING)

    image = Image.new("RGB", (width, height), random_color(rng=rng))
    draw = ImageDraw.Draw(image)
    x = (width - (right - left)) / 2 - left
    y = (height - (bottom - top)) / 2 - top
    draw.text((x, y), code, fill=TEXT_COLOR, font=font)

    for _ in range(STRIKE_LINES):
        start = (rng.randint(0, width // 4), rng.randint(height // 4, height * 3 // 4))
        end = (rng.randint(width * 3 // 4, width), rng.randint(height // 4, height * 3 // 4))
        draw.line([start, end], fill=random_color(0, 120, rng=rng), width=rng.randint(2, 3))

    return image
