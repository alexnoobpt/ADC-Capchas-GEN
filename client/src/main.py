"""Ponto de entrada único: login primeiro e depois o menu principal."""

from src.captchas import main as captchas
from src.captchas.imagem import menu_imagem
from src.storage.db import init_db
from src.user.main import authenticate


def menu_principal(session):
    """Devolve True se o utilizador quiser sair da aplicação, False se terminar a sessão."""
    while True:
        print(f"\nMenu principal ({session['username']})")
        print("1. Ver / baixar imagem de um CAPTCHA")
        print("2. Gerir CAPTCHAs")
        print("3. Terminar sessão")
        print("4. Sair")
        opcao = input("Escolha uma opção: ").strip()
        if opcao == "1":
            menu_imagem(session["user_id"])
        elif opcao == "2":
            captchas.main(session["user_id"])
        elif opcao == "3":
            print("Sessão terminada.")
            return False
        elif opcao == "4":
            print("Até mais!")
            return True
        else:
            print("Opção inválida.")


def main():
    init_db()
    while True:
        session = authenticate()
        if session is None or menu_principal(session):
            break


if __name__ == "__main__":
    main()
