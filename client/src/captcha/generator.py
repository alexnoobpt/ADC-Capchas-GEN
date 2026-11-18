"""Criação da imagem do CAPTCHA com Pillow e download para o computador."""

import re
from pathlib import Path

from PIL import Image, ImageDraw

from src.config.settings import DEFAULT_TEXT, IMAGE_HEIGHT, IMAGE_WIDTH, TEXT_COLOR, Color
from src.utils.colors import random_color

# Pasta de downloads do utilizador (ex.: C:\Users\nome\Downloads)
DOWNLOADS_DIR = Path.home() / "Downloads"


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

    # Mede o texto para o centrar na imagem
    left, top, right, bottom = draw.textbbox((0, 0), text)
    x = (width - (right - left)) / 2 - left
    y = (height - (bottom - top)) / 2 - top

    draw.text((x, y), text, fill=text_color)
    return image


def _safe_filename(name: str) -> str:
    """Limpa o nome para ser usado como nome de ficheiro.

    Os caracteres que não sejam letras, números, `_` ou `-` são
    substituídos por `_`. Se o resultado ficar vazio, devolve "captcha".
    """
    cleaned = re.sub(r"[^\w\-]", "_", name).strip("_")
    return cleaned or "captcha"


def _unique_path(path: Path) -> Path:
    """Devolve um caminho que ainda não existe, para não sobrescrever ficheiros.

    Se `captcha.png` já existir, tenta `captcha_1.png`, `captcha_2.png`, etc.
    """
    if not path.exists():
        return path

    counter = 1
    while True:
        candidate = path.with_name(f"{path.stem}_{counter}{path.suffix}")
        if not candidate.exists():
            return candidate
        counter += 1


def download_captcha(
    image: Image.Image,
    filename: str = "captcha",
    folder: Path | str = DOWNLOADS_DIR,
) -> Path:
    """Guarda o CAPTCHA como PNG na pasta de downloads e devolve o caminho.

    Se `folder` não for indicado, é usado a pasta Downloads do utilizador. 
    Se já existir um ficheiro com o mesmo nome,
    é acrescentado um número ao nome em vez de o sobrescrever.
    """
    folder = Path(folder)
    folder.mkdir(parents=True, exist_ok=True)

    path = _unique_path(folder / f"{_safe_filename(filename)}.png")
    image.save(path, format="PNG")
    return path
