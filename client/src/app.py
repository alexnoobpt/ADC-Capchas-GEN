"""Ponto de entrada: gera um CAPTCHA e guarda-o em PNG."""

from src.captcha.generator import generate_captcha
from src.storage.file_storage import save_image


def main() -> None:
    image = generate_captcha()
    path = save_image(image)
    print(f"CAPTCHA guardado em {path}")


if __name__ == "__main__":
    main()
