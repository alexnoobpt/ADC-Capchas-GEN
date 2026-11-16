def validar_palavra_passe(password):   
    while len(password)!=6:
            password=input("Palavra-passe deve ter exatamente 6 caracteres, tente novamente: ")
    return password

def criar_conta():
    print("Crie uma nova conta!")
    utilizador=input("Escolha o nome de um utilizador: ")
    while utilizador==" ":
        utilizador=input("O nome não pode estar vazio.Tente novamente: ")
    password=validar_palavra_passe(input("Crie uma palavra-passe de 6-caracteres: "))
    print("Conta criada com sucesso!")