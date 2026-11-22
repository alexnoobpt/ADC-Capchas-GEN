from . import dados


def ver_comunidade(user_id, apenas_outros=True):
    titulo = "Captchas de Outros Utilizadores" if apenas_outros else "Todos os Captchas da Comunidade"
    print(f"\n--- {titulo} ---")

    excluir = user_id if apenas_outros else None
    publicacoes = dados.listar_publicacoes_comunidade(excluir_user_id=excluir)

    if not publicacoes:
        print("Não existem publicações disponíveis de momento.")
        return

    mapa_pubs = {}
    for p in publicacoes:
        mapa_pubs[p["publicacao_id"]] = p
        print(
            f"\nID Publicação: {p['publicacao_id']} | Título: {p['title']}\n"
            f"  Autor: {p['autor']} | Captcha: {p['captcha_nome']} ({p['type_name']} - {p['difficulty']})\n"
            f"  Descrição: {p['description'] or 'Sem descrição'}\n"
            f"  Publicado em: {p['created_at']}"
        )

    escolha = input("\nQueres experimentar resolver algum? Introduz o ID da publicação (ou Enter para voltar): ").strip()
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

    _testar_captcha(pub)


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