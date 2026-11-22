"""Configuração central do gerador de CAPTCHAs."""

from pathlib import Path

Color = tuple[int, int, int]

IMAGE_WIDTH: int = 200
IMAGE_HEIGHT: int = 80

DEFAULT_TEXT: str = "CAPTCHA"
TEXT_COLOR: Color = (0, 0, 0)

# Intervalo de cada canal da cor de fundo (tons claros, para o texto escuro ser legível)
BACKGROUND_MIN: int = 180
BACKGROUND_MAX: int = 255

OUTPUT_DIR: Path = Path("output")
OUTPUT_FILENAME: str = "captcha.png"

# Pasta dos downloads. None = descobrir automaticamente a pasta Downloads do utilizador
DOWNLOADS_DIR: Path | None = None
