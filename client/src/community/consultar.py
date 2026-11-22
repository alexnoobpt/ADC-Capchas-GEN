from . import dados


def _formatar_meu_voto(voto):
    if voto == 1:
        return " | O teu voto: Like"
    if voto == -1:
        return " | O teu voto: Dislike"
    return ""


def ver_comunidade(user_id, apenas_outros=True):
    titulo = "Captchas de Outros Utilizadores" if apenas_outros else "Todos os Captchas da Comunidade"
    print(f"\n--- {titulo} ---")

    publicacoes = dados.listar_publicacoes_comunidade(user_id, apenas_outros=apenas_outros)

    if not publicacoes:
        print("Não existem publicações disponíveis de momento.")
        return

    mapa_pubs = {}
    for p in publicacoes:
        mapa_pubs[p["publicacao_id"]] = p
        voto_str = _formatar_meu_voto(p["meu_voto"])
        print(
            f"\nID Publicação: {p['publicacao_id']} | Título: {p['title']}\n"
            f"  Autor: {p['autor']} | Captcha: {p['captcha_nome']} ({p['type_name']} - {p['difficulty']})\n"
            f"  Descrição: {p['description'] or 'Sem descrição'}\n"
            f"  Likes: {p['likes']} | Dislikes: {p['dislikes']}{voto_str}\n"
            f"  Publicado em: {p['created_at']}"
        )

    escolha = input("\nIntroduz o ID da publicação para interagir (ou Enter para voltar): ").strip()
    if not escolha:
        return

    try:
        pub_id = int(escolha)
    except ValueError:
        print("ID inválido.")
        return

    pub = mapa_pubs.get(pub_id)
    if not pub:
        print("Publicação não encontrada na lista.")
        return

    _menu_interacao(pub, user_id)


def _menu_interacao(pub, user_id):
    while True:
        print(f"\n--- {pub['title']} (por {pub['autor']}) ---")
        print("1. Resolver captcha")
        print("2. Dar Like")
        print("3. Dar Dislike")
        print("4. Remover o meu voto")
        print("0. Voltar")

        opcao = input("Escolhe uma opção: ").strip()

        if opcao == "1":
            _testar_captcha(pub)
        elif opcao == "2":
            if dados.votar_publicacao(pub["publicacao_id"], user_id, 1):
                print("Like registado!")
            else:
                print("Erro ao registar like.")
        elif opcao == "3":
            if dados.votar_publicacao(pub["publicacao_id"], user_id, -1):
                print("Dislike registado!")
            else:
                print("Erro ao registar dislike.")
        elif opcao == "4":
            if dados.remover_voto(pub["publicacao_id"], user_id):
                print("Voto removido!")
            else:
                print("Ainda não tinhas votado nesta publicação.")
        elif opcao == "0":
            break
        else:
            print("Opção inválida.")


def _testar_captcha(pub):
    print(f"\n=== Desafio: {pub['title']} ({pub['type_name']}) ===")
    if pub["challenge_data"]:
        print(f"Desafio: {pub['challenge_data']}")

    imagens = dados.listar_imagens_captcha(pub["captcha_id"])
    if imagens:
        print("Imagens associadas:")
        for img in imagens:
            print(f"  - {img['image_path']}")

    resposta = input("A tua resposta: ").strip()
    if resposta.lower() == pub["solution"].strip().lower():
        print("Correto! Resolveste o captcha.")
    else:
        print("Incorreto. Tenta novamente mais tarde!")