from src.captchas.dados import captchas

DIFICULDADES = {"1": "Fácil", "2": "Médio", "3": "Difícil"}
TIPOS = {"1": "Texto", "2": "Emoji", "3": "Matemático"}


def ver_captchas():
    if not captchas:
        print("Nenhum Captcha criado ainda.")
        return

    for dificuldade, nome_dificuldade in DIFICULDADES.items():
        do_nivel = [c for c in captchas if c[1] == dificuldade]
        if not do_nivel:
            continue
        print(f"--- {nome_dificuldade} ---")
        for captcha in do_nivel:
            print(f"Nome: {captcha[0]}, Tipo: {TIPOS[captcha[2]]}")
