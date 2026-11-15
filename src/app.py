import sqlite3

conn=sqlite3.connect("database/contas.db")
cursor=conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS contas (
    utilizador TEXT PRIMARY KEY NOT NULL,
    password TEXT NOT NULL
    )
""")
conn.commit()

def menu():
  
    print(r"""
         _____            __      __              
        / ____|           | |     | |              
        | |     __ _ _ __ | |_ ___| |__   __ _ ___ 
        | |    / _` | '_ \| __/ __| '_ \ / _` / __|
        | |___| (_| | |_) | || (__| | | | (_| \__ \
         \_____\__,_| .__/ \__\___|_| |_|\__,_|___/
                    | |                            
                    |_| Maker""") 
    
    print("")                   
    print("ESCOLHA 1 - Iniciar Sessão")
    print("ESCOLHA 2 - Criar Conta") 
    print("ESCOLHA 3 - Sair")
    opcao=input("Escolha uma opção: ") 
    return opcao

def validar_palavra_passe(password):   
    while len(password)!=6:
            password=input("Palavra-passe deve ter exatamente 6 caracteres, tente novamente: ")
    return password

def iniciar_sessao():
    print("Inicie a sessão!")
    utilizador=input("Nome do Utilizador: ")
    cursor.execute(
        "SELECT * FROM contas WHERE utilizador = ?",
        (utilizador,)
    )
    conta=cursor.fetchone()
    if conta is None:
        print("Esse utilizador não existe")
        return

    password=input("Palavra-passe: ")
    if conta[1]==password:
        print("Sessão iniciado com sucesso!")
    else:
        print("Palavra passe errada, por favor, tente novamente!")

def criar_conta():
    print("Crie uma nova conta!")
    utilizador=input("Escolha o nome de um utilizador: ")
    while utilizador==" ":
        utilizador=input("O nome não pode estar vazio.Tente novamente: ")
    cursor.execute(
            "SELECT * FROM contas WHERE utilizador = ?",
            (utilizador,)
        )
    if cursor.fetchone():
        print("Este utilizador já existe!")
        return
    
    password=validar_palavra_passe(input("Crie uma palavra-passe de 6-caracteres: "))
    cursor.execute(
        "INSERT INTO contas VALUES(?,?)",
        (utilizador,password)
    )
    conn.commit()
    print("Conta criada com sucesso!")
    
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
    conn.close()
