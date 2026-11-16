"""Gravação das imagens no disco."""

from pathlib import Path

from PIL import Image

from src.config.settings import OUTPUT_DIR, OUTPUT_FILENAME


def save_image(
    image: Image.Image,
    output_dir: Path = OUTPUT_DIR,
    filename: str = OUTPUT_FILENAME,
) -> Path:
    """Guarda a imagem em PNG dentro de `output_dir` e devolve o caminho do ficheiro."""
    output_dir.mkdir(parents=True, exist_ok=True)
    path = output_dir / filename
    image.save(path, format="PNG")
    return path
