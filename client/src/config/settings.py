"""Configuração central do gerador de CAPTCHAs."""

from pathlib import Path

# Tipo de cor RGB: (vermelho, verde, azul), cada valor entre 0 e 255
Color = tuple[int, int, int]

# Dimensões da imagem (em píxeis)
IMAGE_WIDTH: int = 200
IMAGE_HEIGHT: int = 80

# Texto
DEFAULT_TEXT: str = "CAPTCHA"
TEXT_COLOR: Color = (0, 0, 0)

# Intervalo de cada canal da cor de fundo (tons claros, para o texto escuro ser legível)
BACKGROUND_MIN: int = 180
BACKGROUND_MAX: int = 255

# Saída
OUTPUT_DIR: Path = Path("output")
OUTPUT_FILENAME: str = "captcha.png"

# Pasta dos downloads. None = descobrir automaticamente a pasta Downloads do utilizador
DOWNLOADS_DIR: Path | None = None
