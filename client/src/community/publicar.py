from . import dados


def publicar_captcha(user_id):
    print("\n--- Publicar Captcha na Comunidade ---")
    captchas = dados.listar_captchas_do_utilizador(user_id)

    if not captchas:
        print("Ainda não tens captchas criados para publicar.")
        return

    for c in captchas:
        print(f"[{c['id']}] {c['name']} | Tipo: {c['type_name']} | Dificuldade: {c['difficulty']}")

    try:
        captcha_id = int(input("\nID do captcha a publicar (0 para cancelar): "))
    except ValueError:
        print("ID inválido.")
        return

    if captcha_id == 0:
        return

    titulo = input("Título da publicação: ").strip()
    if not titulo:
        print("O título é obrigatório.")
        return

    descricao = input("Descrição (opcional): ").strip()

    if dados.criar_publicacao(user_id, captcha_id, titulo, descricao):
        print("Captcha publicado na comunidade com sucesso!")
    else:
        print("Não foi possível publicar. Verifica se o ID pertence aos teus captchas.")