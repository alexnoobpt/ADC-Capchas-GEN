from .consultar import ver_comunidade
from .editar import editar_publicacao
from .publicar import publicar_captcha
from .retirar import retirar_captcha


def menu_comunidade(user_id):
    while True:
        print("\n====== COMUNIDADE DE CAPTCHAS ======")
        print("1. Ver captchas de outros utilizadores")
        print("2. Ver todos os captchas da comunidade")
        print("3. Colocar (publicar) um captcha meu")
        print("4. Editar uma publicação minha")
        print("5. Retirar um captcha da comunidade")
        print("0. Voltar")

        opcao = input("Escolhe uma opção: ").strip()

        if opcao == "1":
            ver_comunidade(user_id, apenas_outros=True)
        elif opcao == "2":
            ver_comunidade(user_id, apenas_outros=False)
        elif opcao == "3":
            publicar_captcha(user_id)
        elif opcao == "4":
            editar_publicacao(user_id)
        elif opcao == "5":
            retirar_captcha(user_id)
        elif opcao == "0":
            break
        else:
            print("Opção inválida.")