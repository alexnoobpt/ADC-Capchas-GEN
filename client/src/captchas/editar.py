from src.captchas import desafios, repositorio
from src.captchas.consultar import ver_captchas


def _pedir_nome(user_id, captcha):
    novo_nome=input("Novo nome do Captcha: ").strip()
    if not novo_nome:
        print("Pelo menos um nome")
        return None
    outro=repositorio.obter(user_id, novo_nome)
    if outro and outro["id"]!=captcha["id"]:
        print("Esse nome já se encontra registrado!")
        return None
    return novo_nome


def _pedir_dificuldade():
    dificuldade=input("Nova dificuldade (1-Fácil, 2-Médio, 3-Difícil): ")
    if dificuldade not in ["1", "2", "3"]:
        print("Dificuldade inválida.")
        return None
    return dificuldade


def _pedir_tipo():
    tipo=input("Novo tipo de Captcha (1-Texto, 2-Emoji, 3-Matemático): ")
    if tipo not in ["1", "2", "3"]:
        print("Tipo de Captcha inválido.")
        return None
    return tipo


def editar_captcha(user_id):
    if not repositorio.listar(user_id):
        print("Nenhum Captcha criado ainda.")
        return
    ver_captchas(user_id)
    nome_captcha=input("Digite o nome do Captcha que deseja editar: ").strip()
    captcha=repositorio.obter(user_id, nome_captcha)
    if captcha is None:
        print("Captcha não encontrado.")
        return

    print("Captcha encontrado. O que deseja editar?")
    print("1 - Editar nome")
    print("2 - Editar dificuldade")
    print("3 - Editar tipo")
    print("4 - Editar tudo")
    opcao=input("Escolha uma opção: ").strip()
    if opcao not in ["1", "2", "3", "4"]:
        print("Opção inválida.")
        return

    novo={"nome": captcha["nome"], "dificuldade": captcha["dificuldade"], "tipo": captcha["tipo"]}
    if opcao in ["1", "4"]:
        novo["nome"]=_pedir_nome(user_id, captcha)
    if opcao in ["2", "4"] and novo["nome"]:
        novo["dificuldade"]=_pedir_dificuldade()
    if opcao in ["3", "4"] and novo["nome"] and novo["dificuldade"]:
        novo["tipo"]=_pedir_tipo()
    if not all(novo.values()):
        return

    if (novo["dificuldade"], novo["tipo"]) != (captcha["dificuldade"], captcha["tipo"]):
        # O desafio antigo deixa de corresponder à nova dificuldade/tipo
        captcha["desafio"], captcha["solucao"] = desafios.gerar(novo["tipo"], novo["dificuldade"])
    captcha.update(novo)

    try:
        repositorio.atualizar(captcha)
    except repositorio.NomeRepetido:
        print("Esse nome já se encontra registrado!")
        return
    print("Captcha atualizado com sucesso!")
