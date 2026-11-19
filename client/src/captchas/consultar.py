from dados import captchas

def ver_captchas():
    if not captchas:
        print("Nenhum Captcha criado ainda.")
        return
    
    for i, captcha in enumerate(captchas):
        print(f"{i+1}-Nome: {captcha[0]}, Dificuldade: {captcha[1]}, Tipo: {captcha[2]}")
