from src.captchas.criar import criar_captcha
from src.captchas.consultar import ver_captchas
from src.captchas.editar import editar_captcha
from src.captchas.eliminar import eliminar_captcha
from src.storage.db import init_db
from src.user.main import authenticate

def menu_criação():
    print("Menu de Criação Captcha MAKER")
    print("1. Criar Captcha")
    print("2. Ver Captchas Criados")
    print("3. Editar Captcha")
    print("4. Eliminar Captchas")
    print("5. Voltar")

def main(user_id):
    while True:
        menu_criação()
        try:
            opcao=int(input("Escolha uma opção: "))
        except ValueError:
            print("Por favor, introduza um número válido.")
            continue
        if opcao==1:
            criar_captcha(user_id)
        elif opcao==2:
            ver_captchas(user_id)
        elif opcao==3:
            editar_captcha(user_id)
        elif opcao==4:
            eliminar_captcha(user_id)
        elif opcao==5:
            print("A voltar...")
            break
        else:
            print("Opção inválida.")

if __name__ == "__main__":
    init_db()
    session = authenticate()
    if session is not None:
        main(session["user_id"])
