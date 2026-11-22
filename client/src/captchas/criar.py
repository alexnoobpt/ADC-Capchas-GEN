from src.captchas import desafios, repositorio


def criar_captcha(user_id):
    nome=input("Nome do Captcha: ").strip()
    if not nome:
        print("Pelo menos um nome")
        return
    if repositorio.obter(user_id, nome):
        print("Esse nome já se encontra registrado!")
        return
    dificuldade=input("Dificuldade (1-Fácil, 2-Médio, 3-Difícil): ")
    if dificuldade not in ["1", "2", "3"]:
        print("Dificuldade inválida. Por favor, escolha entre 1, 2 ou 3.")
        return
    tipo_de_captcha=input("Tipo de Captcha (1-Texto, 2-Emoji, 3-Matemático): ")
    if tipo_de_captcha not in ["1", "2", "3"]:
        print("Tipo de Captcha inválido. Por favor, escolha entre 1, 2 ou 3.")
        return

    desafio, solucao = desafios.gerar(tipo_de_captcha, dificuldade)
    desafios.resolver(tipo_de_captcha, desafio, solucao)

    try:
        repositorio.criar(user_id, nome, dificuldade, tipo_de_captcha, desafio, solucao)
    except repositorio.NomeRepetido:
        print("Esse nome já se encontra registrado!")
        return
    print("Captcha criado com sucesso!")
