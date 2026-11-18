from dados import captchas
from consultar import ver_captchas

def editar_captcha():
    if not captchas:
            print("Nenhum Captcha criado ainda.")
            return
    ver_captchas()
    nome_captcha=input("Digite o nome do Captcha que deseja editar: ")
    encontrado=False
    for c in captchas:
        if c[0]==nome_captcha:
            encontrado=True
            print("Captcha encontrado. O que deseja editar?")
            print("1. Nome")
            print("2. Dificuldade")
            print("3. Tipo")
            print("4.Tudo")
            try:
                opcao=int(input("Escolha uma opção: "))
            except ValueError:
                print("Opção inválida.")
                return

            novo_nome=c[0]
            nova_dificuldade=c[1]
            novo_tipo=c[2]
            if opcao==1:
                novo_nome=input("Novo nome do Captcha: ")
                if novo_nome==" ":
                    print("Pelo menos um nome")
                    return
                for i in captchas:
                        if i!=c and i[0]==novo_nome:
                            print("Esse nome já se encontra registrado!")
                            return

            elif opcao==2:
                nova_dificuldade=input("Nova dificuldade (1-Fácil, 2-Médio, 3-Difícil): ")
                if nova_dificuldade not in ["1", "2", "3"]:
                    print("Dificuldade inválida.")
                    return 
                                   
            elif opcao==3:
                novo_tipo=input("Novo tipo de Captcha (1-Texto, 2-Emoji, 3-Matemático): ")
                if novo_tipo not in ["1", "2", "3"]:
                    print("Tipo de Captcha inválido.")
                    return 
                
            elif opcao==4:
                novo_nome=input("Novo nome do Captcha: ")
                if novo_nome==" ":
                    print("Pelo menos um nome")
                    return
                for i in captchas:
                    if i!=c and i[0]==novo_nome:
                        print("Esse nome já se encontra registrado!")
                        return
                nova_dificuldade=input("Nova dificuldade (1-Fácil, 2-Médio, 3-Difícil): ")
                if nova_dificuldade not in ["1", "2", "3"]:
                    print("Dificuldade inválido.")
                    return 
                novo_tipo=input("Novo tipo de Captcha (1-Texto, 2-Emoji, 3-Matemático): ")
                if novo_tipo not in ["1", "2", "3"]:
                    print("Tipo de Captcha inválido.")
                    return 
            else:
                print("Por favor, um número válido")
                return
            
            c[0]=novo_nome
            c[1]=nova_dificuldade
            c[2]=novo_tipo

            print("Captcha atualizado com sucesso!")
            break
    if not encontrado:
        print("Captcha não encontrado.")
