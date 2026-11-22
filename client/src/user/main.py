from src.user.menu import menu
from src.user.accounts import create_account
from src.user.login import log_in
from src.storage.db import init_db


def authenticate():
    """Mostra o menu de login até haver sessão; devolve None se o utilizador sair."""
    while True:
        option=menu()
        if option=="1":
            session=log_in()
            if session is not None:
                print("Access granted")
                return session
        elif option=="2":
            create_account()
        elif option=="3":
            print("Exiting...")
            return None
        else:
            print("Error, please try again!")


def main():
    init_db()
    authenticate()


if __name__ == "__main__":
    main()
