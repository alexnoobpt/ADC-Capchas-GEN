import random

from src.captcha.generator import generate_text_captcha
from src.captchas.dados import captchas
from src.storage.file_storage import download_image
from src.utils.terminal import print_image


def imagem_do_captcha(captcha):
    codigo = captcha[3]
    # Mesma semente = mesma imagem sempre que o CAPTCHA é mostrado ou baixado
    return generate_text_captcha(codigo, random.Random(codigo))


def menu_imagem():
    de_texto = [c for c in captchas if c[2] == "1" and c[3]]
    if not de_texto:
        print("Ainda não há CAPTCHAs de texto. Por agora só os de texto têm imagem.")
        return

    print("CAPTCHAs com imagem:")
    for c in de_texto:
        print(f"- {c[0]}")
    nome = input("Nome do Captcha: ").strip()
    captcha = next((c for c in de_texto if c[0] == nome), None)
    if captcha is None:
        print("Captcha não encontrado.")
        return

    imagem = imagem_do_captcha(captcha)
    while True:
        print(f"\nCaptcha: {captcha[0]}")
        print("1 - Mostrar no terminal")
        print("2 - Baixar imagem")
        print("3 - Voltar")
        opcao = input("Escolha uma opção: ").strip()
        if opcao == "1":
            if not print_image(imagem):
                print("Este terminal não consegue mostrar a imagem. Use a opção 2 para a baixar.")
        elif opcao == "2":
            caminho = download_image(imagem, captcha[0])
            print(f"Download concluído em {caminho}")
        elif opcao == "3":
            return
        else:
            print("Opção inválida.")
