from src.captchas import repositorio

DIFICULDADES = {"1": "Fácil", "2": "Médio", "3": "Difícil"}


def ver_captchas(user_id):
    captchas = repositorio.listar(user_id)
    if not captchas:
        print("Nenhum Captcha criado ainda.")
        return

    for dificuldade, nome_dificuldade in DIFICULDADES.items():
        do_nivel = [c for c in captchas if c["dificuldade"] == dificuldade]
        if not do_nivel:
            continue
        print(f"--- {nome_dificuldade} ---")
        for captcha in do_nivel:
            print(f"Nome: {captcha['nome']}, Tipo: {repositorio.NOMES_TIPO[captcha['tipo']]}")
