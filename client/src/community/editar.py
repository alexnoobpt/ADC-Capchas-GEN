from . import dados


def editar_publicacao(user_id):
    print("\n--- Editar Publicação ---")
    publicacoes = dados.listar_minhas_publicacoes(user_id)

    if not publicacoes:
        print("Não tens publicações na comunidade.")
        return

    for p in publicacoes:
        print(
            f"[{p['publicacao_id']}] {p['title']} | "
            f"Captcha: {p['captcha_nome']} | "
            f"Likes: {p['likes']} | Dislikes: {p['dislikes']}"
        )

    try:
        pub_id = int(input("\nID da publicação a editar (0 para cancelar): "))
    except ValueError:
        print("ID inválido.")
        return

    if pub_id == 0:
        return

    novo_titulo = input("Novo título: ").strip()
    if not novo_titulo:
        print("O título não pode ficar vazio.")
        return

    nova_descricao = input("Nova descrição: ").strip()

    if dados.atualizar_publicacao(pub_id, user_id, novo_titulo, nova_descricao):
        print("Publicação atualizada com sucesso!")
    else:
        print("Publicação não encontrada ou sem permissão para editar.")