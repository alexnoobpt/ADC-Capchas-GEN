from menu import menu
from contas import criar_conta
from sessao import iniciar_sessao

def main():
    while True:
        opcao=menu()
        if opcao=="1":
            iniciar_sessao()
        elif opcao=="2":
            criar_conta()
        elif opcao=="3":
            print("A sair...")
            break
        else:
            print("Erro, por favor, tente novamente!")
            

if __name__ == "__main__":
    main()
