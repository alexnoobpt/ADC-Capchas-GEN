import os
import shutil

from PIL import Image

HALF_BLOCK = "▀"
RESET = "\x1b[0m"


def image_to_ansi(image: Image.Image, max_width: int | None = None) -> str:
    """Converte a imagem em texto colorido: cada carácter ▀ mostra 2 píxeis (cima e baixo)."""
    if max_width is None:
        max_width = shutil.get_terminal_size().columns - 1
    width = max(1, min(image.width, max_width))
    height = max(2, round(image.height * width / image.width))
    height += height % 2
    small = image.convert("RGB").resize((width, height), Image.Resampling.LANCZOS)

    lines = []
    for y in range(0, height, 2):
        cells = []
        for x in range(width):
            top = small.getpixel((x, y))
            bottom = small.getpixel((x, y + 1))
            cells.append(f"\x1b[38;2;{top[0]};{top[1]};{top[2]}m\x1b[48;2;{bottom[0]};{bottom[1]};{bottom[2]}m{HALF_BLOCK}")
        lines.append("".join(cells) + RESET)
    return "\n".join(lines)


def print_image(image: Image.Image) -> bool:
    """Mostra a imagem no terminal; devolve False se o terminal não a conseguir mostrar."""
    if os.name == "nt":
        # Ativa as cores ANSI na consola do Windows
        os.system("")
    try:
        print(image_to_ansi(image))
    except UnicodeEncodeError:
        return False
    return True
