import random
import string

TEXTO, EMOJI, MATEMATICO = "1", "2", "3"

# Sem £ e §: a fonte das imagens não tem esses símbolos
SIMBOLOS = "!@#$%&?*+^~»"
TAMANHO_CODIGO = {"1": 6, "2": 12, "3": 18}

CATEGORIAS_EMOJI = {
    "Animais": ["🐺", "🐻", "🐘", "🦔", "🫍", "🐦‍⬛", "🐠", "🐱", "🐭", "🐹", "🐰"],
    "Comida": ["🥗", "🍖", "🥡", "🥠", "🍠", "🥞", "🍕", "🫐", "🥬", "🌶️", "🍏"],
    "Paisagens": ["🛤️", "🏕️", "🏞️", "🛣️", "🏜️", "🏘️", "🏙️", "🌉", "🌁", "🌃", "🌅", "🌇"],
}
EMOJI_POR_DIFICULDADE = {"1": ("Animais", 3), "2": ("Comida", 5), "3": ("Paisagens", 7)}
TOTAL_OPCOES_EMOJI = 9

VARIACAO_EMOJI = "️"


def gerar(tipo, dificuldade):
    """Devolve (desafio, solucao) para o tipo e dificuldade dados."""
    if tipo == TEXTO:
        return gerar_texto(dificuldade)
    if tipo == EMOJI:
        return gerar_emoji(dificuldade)
    return gerar_matematico(dificuldade)


def gerar_texto(dificuldade):
    codigo = "".join(random.choices(string.ascii_letters + string.digits + SIMBOLOS, k=TAMANHO_CODIGO[dificuldade]))
    return {"codigo": codigo}, codigo


def gerar_emoji(dificuldade):
    categoria, quantidade = EMOJI_POR_DIFICULDADE[dificuldade]
    certos = random.sample(CATEGORIAS_EMOJI[categoria], quantidade)
    errados = [e for nome, lista in CATEGORIAS_EMOJI.items() if nome != categoria for e in lista]
    opcoes = certos + random.sample(errados, TOTAL_OPCOES_EMOJI - quantidade)
    random.shuffle(opcoes)
    desafio = {"categoria": categoria, "quantidade": quantidade, "opcoes": opcoes}
    return desafio, sorted(_sem_variacao(e) for e in certos)


def gerar_matematico(dificuldade):
    if dificuldade == "1":
        intervalo, operadores = (1, 10), ["+", "-"]
    elif dificuldade == "2":
        intervalo, operadores = (10, 50), ["+", "-", "*"]
    else:
        intervalo, operadores = (50, 100), ["+", "-", "*", "/"]
    num1, num2 = random.randint(*intervalo), random.randint(*intervalo)
    operador = random.choice(operadores)
    resultados = {"+": num1 + num2, "-": num1 - num2, "*": num1 * num2, "/": round(num1 / num2, 2)}
    return {"num1": num1, "operador": operador, "num2": num2}, resultados[operador]


def resolver(tipo, desafio, solucao):
    """Mostra o desafio, lê a resposta e diz se está certa. Devolve True se estiver."""
    if tipo == TEXTO:
        return _resolver_texto(desafio["codigo"])
    if tipo == EMOJI:
        return _resolver_emoji(desafio, solucao)
    return _resolver_matematico(desafio, solucao)


def _resolver_texto(codigo):
    print("Captcha: ", codigo)
    perguntas = [
        ("Quantas letras em minúsculo tem o captcha? ", sum(1 for c in codigo if c.islower())),
        ("Quantas letras em maiúsculo tem o captcha? ", sum(1 for c in codigo if c.isupper())),
        ("Quantas vogais tem o captcha? ", sum(1 for c in codigo if c in "aeiouAEIOU")),
        ("Quantas consoantes tem o captcha? ", sum(1 for c in codigo if c.isalpha() and c not in "aeiouAEIOU")),
        ("Quantos números tem o captcha? ", sum(1 for c in codigo if c.isdigit())),
        ("Quantos símbolos tem o captcha? ", sum(1 for c in codigo if c in SIMBOLOS)),
    ]
    pergunta, resposta_certa = random.choice(perguntas)
    print(pergunta)
    try:
        resposta = int(input("Introduza a resposta: "))
    except ValueError:
        print("Por favor, introduza um número válido")
        return False
    return _resultado(resposta == resposta_certa)


def _resolver_emoji(desafio, solucao):
    quantidade = desafio["quantidade"]
    print(f"Escolha {quantidade} emojis da categoria {desafio['categoria']}: ")
    print("Opções:", " | ".join(desafio["opcoes"]))
    resposta = sorted(_ler_emojis(input("Introduza os emojis escolhidos: "), desafio["opcoes"]))
    if len(resposta) != quantidade:
        print(f"Deve introduzir exatamente {quantidade} emojis!")
        return False
    return _resultado(resposta == solucao)


def _resolver_matematico(desafio, solucao):
    enunciado = f"Resolva a seguinte operação: {desafio['num1']} {desafio['operador']} {desafio['num2']}"
    if desafio["operador"] == "/":
        enunciado += " (arredonde a 2 casas decimais)"
    print(enunciado)
    try:
        resposta = float(input("Introduza a resposta: ").replace(",", "."))
    except ValueError:
        print("Por favor, introduza um número válido")
        return False
    return _resultado(abs(resposta - solucao) < 0.005)


def _resultado(certo):
    print("Resposta correta!" if certo else "Resposta incorreta.")
    return certo


def _sem_variacao(emoji):
    # O seletor U+FE0F perde-se muitas vezes ao escrever ou copiar (🌶️ vs 🌶)
    return emoji.replace(VARIACAO_EMOJI, "")


def _ler_emojis(texto, opcoes):
    """Separa a resposta nos emojis das opções, com ou sem espaços entre eles."""
    conhecidos = sorted({_sem_variacao(o) for o in opcoes}, key=len, reverse=True)
    resto = _sem_variacao(texto).replace("|", "").replace(" ", "")
    encontrados = []
    while resto:
        emoji = next((e for e in conhecidos if resto.startswith(e)), None)
        if emoji is None:
            emoji = resto[0]
        encontrados.append(emoji)
        resto = resto[len(emoji):]
    return encontrados
