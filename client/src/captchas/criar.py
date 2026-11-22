import random
import string
from src.captchas.dados import captchas

def criar_captcha():
    nome=input("Nome do Captcha: ").strip()
    if not nome:
        print("Pelo menos um nome")
        return
    for c in captchas:
        if c[0]==nome:
            print("Esse nome já se encontra registrado!")
            return
    dificuldade=input("Dificuldade (1-Fácil, 2-Médio, 3-Difícil): ")
    if dificuldade not in ["1", "2", "3"]:
        print("Dificuldade inválida. Por favor, escolha entre 1, 2 ou 3.")
        return
    tipo_de_captcha=input("Tipo de Captcha (1-Texto, 2-Emoji, 3-Matemático): ")
    if tipo_de_captcha not in ["1", "2", "3"]:
        print("Tipo de Captcha inválido. Por favor, escolha entre 1, 2 ou 3.")
        return
    if tipo_de_captcha=="1":

        if dificuldade=="1":
            tamanho=6
        elif dificuldade=="2":
            tamanho=12
        else:
            tamanho=18

        codigo="".join(random.choices(string.ascii_letters + string.digits +"!@£#$§%&?*+^~»", k=tamanho))
        
        print("Captcha: ",codigo)

        perguntas=[
            ("Quantas letras em minusculo tem o captcha? ",
            sum(1 for c in codigo if c.islower())),
            ("Quantas letras em maiusculo tem o captcha? ",
            sum(1 for c in codigo if c.isupper())),
            ("Quantas vogais tem o captcha? ",
            sum(1 for c in codigo if c in "aeiouAEIOU")),
            ("Quantas consoantes tem o captcha? ",
            sum(1 for c in codigo if c.isalpha() and c not in "aeiouAEIOU")),
            ("Quantos números tem o captcha? ",
            sum(1 for c in codigo if c.isdigit())),
            ("Quantas simbolos tem o captcha?",
            sum(1 for c in codigo if c in "!@£#$§%&?*+^~»")),
        ]

        pergunta,resposta_certa=random.choice(perguntas)
        print(pergunta)
        try:
            resposta_user=int(input("Introduza a resposta: "))
            if resposta_user==resposta_certa:
                print("Resposta correta!")  
            else:
                print("Resposta incorreta.")
        except ValueError:
            print("Por favor, introduza um número valido")

    elif tipo_de_captcha=="2":
        categorias_emoji={
            "Animais": ["🐺","🐻","🐘","🦔","🫍","🐦‍⬛","🐠", "🐱", "🐭", "🐹", "🐰"],
            "Comida": ["🥗","🍖","🥡","🥠","🍠","🥞","🍕","🫐","🥬","🌶️","🍏"],
            "Paisagens": ["🛤️","🏕️","🏞️","🛣️","🏜️","🏘️","🏙️","🌉","🌁","🌃","🌅","🌇"]
        }

        if dificuldade=="1":
            categoria="Animais"
            quantidade=3
        elif dificuldade=="2":
            categoria="Comida"
            quantidade=5
        else:
            categoria="Paisagens"
            quantidade=7

        certos=random.sample(categorias_emoji[categoria], quantidade)
        errados=[]
        for nome_categoria,lista in categorias_emoji.items():
            if nome_categoria!=categoria:
                errados.extend(lista)

        opcoes=certos+random.sample(errados,9-quantidade)
        random.shuffle(opcoes)  
        pedido=f"Escolha {quantidade} emojis da categoria {categoria}: "
        resposta_certa=(sorted(certos))
        print(pedido)
        print("Opções:", " | ".join(opcoes))
        resposta=input("Introduza os emojis escolhidos: ")
        resposta_user=(sorted(resposta.replace("|","").split()))
        if len(resposta_user)!=quantidade:
            print(f"Deve introduzir exatamente {quantidade} emojis!")
        elif resposta_user==resposta_certa:
            print("Resposta correta!")
        else:
            print("Resposta incorreta.")
    
    elif tipo_de_captcha=="3":
        if dificuldade=="1":
            num1=random.randint(1,10)
            num2=random.randint(1,10)
            operador=random.choice(["+","-"])
        elif dificuldade=="2":
            num1=random.randint(10,50)
            num2=random.randint(10,50)
            operador=random.choice(["+","-","*"])
        else:
            num1=random.randint(50,100)
            num2=random.randint(50,100)
            operador=random.choice(["+","-","*","/"])

        codigo=f"Resolva a seguinte operação: {num1} {operador} {num2}"
        if operador=="+":
            resposta_certa=num1+num2
        elif operador=="-":
            resposta_certa=num1-num2
        elif operador=="*":
            resposta_certa=num1*num2
        else:
            resposta_certa=round(num1/num2,2)

        print(codigo)
        try:
            resposta_user=float(input("Introduza a resposta: "))
            if resposta_user==resposta_certa:
                print("Resposta correta!")  
            else:
                print("Resposta incorreta.")
        except ValueError:
            print("Por favor, introduza um número valido")
        

    captcha=[nome, dificuldade, tipo_de_captcha]
    captchas.append(captcha)
    print("Captcha criado com sucesso!")
