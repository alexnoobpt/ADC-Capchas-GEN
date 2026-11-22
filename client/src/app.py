"""Ponto de entrada: gera um CAPTCHA, guarda-o em PNG e permite fazer download."""

from src.captcha.generator import generate_captcha
from src.storage.file_storage import download_image, save_image


def ask_yes_no(question: str) -> bool:
    """Faz uma pergunta na consola e devolve True se a resposta for sim (s/sim)."""
    return input(f"{question} [s/N]: ").strip().lower() in {"s", "sim"}


def main() -> None:
    image = generate_captcha()
    path = save_image(image)
    print(f"CAPTCHA guardado em {path}")

    if ask_yes_no("Fazer download do CAPTCHA?"):
        download_path = download_image(image)
        print(f"Download concluído em {download_path}")


if __name__ == "__main__":
    main()