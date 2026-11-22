from src.captchas.criar import criar_captcha
from src.captchas.consultar import ver_captchas
from src.captchas.editar import editar_captcha
from src.captchas.eliminar import eliminar_captcha

def menu_criação():
    print("Menu de Criação Captcha MAKER")
    print("1. Criar Captcha")
    print("2. Ver Captchas Criados")
    print("3. Editar Captcha")
    print("4. Eliminar Captchas")
    print("5. Voltar")

def main():
    while True:
        menu_criação()
        try:
            opcao=int(input("Escolha uma opção: "))
        except ValueError:
            print("Por favor, introduza um número válido.")
            continue
        if opcao==1:
            criar_captcha()
        elif opcao==2:
            ver_captchas()
        elif opcao==3:
            editar_captcha()
        elif opcao==4:
            eliminar_captcha()
        elif opcao==5:
            print("A voltar...")
            break
        else:
            print("Opção inválida.")

if __name__ == "__main__":
    main()

