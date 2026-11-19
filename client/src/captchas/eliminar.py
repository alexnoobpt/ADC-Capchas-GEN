from dados import captchas
from consultar import ver_captchas 

def eliminar_captcha():
    if not captchas:
        print("Nenhum Captcha criado ainda.")
        return
    
    ver_captchas()
    nome_captcha=input("Digite o nome do Captcha que deseja eliminar: ")
    encontrado=False
    for c in captchas:
        if c[0]==nome_captcha:
                encontrado=True
                print("Tem certeza que deseja eliminar este Captcha? (s/n)")
                resposta=input().lower()
                if resposta=="s":
                    captchas.remove(c)
                    print("Captcha eliminado com sucesso!")
                elif resposta=="n":
                    print("Operação cancelada.")
                else:
                    print("Opção inválida. Operação cancelada.")
                break
    if not encontrado:
        print("Captcha não encontrado.")