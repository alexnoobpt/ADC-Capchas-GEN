from . import dados


def retirar_captcha(user_id):
    print("\n--- Retirar Captcha da Comunidade ---")
    publicacoes = dados.listar_minhas_publicacoes(user_id)

    if not publicacoes:
        print("Não tens nenhum captcha publicado na comunidade.")
        return

    for p in publicacoes:
        print(
            f"[{p['publicacao_id']}] {p['title']} | "
            f"Captcha: {p['captcha_nome']} ({p['difficulty']}) | "
            f"Data: {p['created_at']}"
        )

    try:
        pub_id = int(input("\nID da publicação a retirar (0 para cancelar): "))
    except ValueError:
        print("ID inválido.")
        return

    if pub_id == 0:
        return

    confirmacao = input("Tens a certeza que queres retirar este captcha da comunidade? (s/n): ").strip().lower()
    if confirmacao != "s":
        print("Operação cancelada.")
        return

    if dados.eliminar_publicacao(pub_id, user_id):
        print("Captcha retirado da comunidade com sucesso!")
    else:
        print("Não foi possível retirar. Verifica se o ID te pertence.")