from src.captchas import repositorio
from src.captchas.consultar import ver_captchas


def eliminar_captcha(user_id):
    if not repositorio.listar(user_id):
        print("Nenhum Captcha criado ainda.")
        return

    ver_captchas(user_id)
    nome_captcha=input("Digite o nome do Captcha que deseja eliminar: ").strip()
    captcha=repositorio.obter(user_id, nome_captcha)
    if captcha is None:
        print("Captcha não encontrado.")
        return

    print("Tem certeza que deseja eliminar este Captcha? (s/n)")
    resposta=input().lower()
    if resposta=="s":
        repositorio.eliminar(captcha["id"])
        print("Captcha eliminado com sucesso!")
    elif resposta=="n":
        print("Operação cancelada.")
    else:
        print("Opção inválida. Operação cancelada.")
