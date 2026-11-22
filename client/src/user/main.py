from client.src.user.menu import menu
from client.src.user.accounts import create_account
from client.src.user.login import log_in
from database.db import init_db

def main():
    init_db()

    while True:
        option=menu()
        if option=="1":
            session=log_in()
            if session is not None:
                print("Acess granted")
        elif option=="2":
            create_account()
        elif option=="3":
            print("Exiting...")
            break
        else:
            print("Error, please try again!")
            

if __name__ == "__main__":
    main()