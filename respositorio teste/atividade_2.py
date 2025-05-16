import requests

usuarios = {
    1: {"email": "usuario1@gmail.com", "senha": "1234"},
    2: {"email": "usuario2@gmail.com", "senha": "abcd"},
    3: {"email": "usuario3@gmail.com", "senha": "senha"},
}

interacoes = {
    "posts_visualizados": 0,
    "comentarios_visualizados": 0,
    "posts_criados": 0,
}

def login():
    print("Bem-vindo ao sistema! Vamos começar com o login.")
    email = input("Digite seu e-mail: ").strip()
    senha = input("Digite sua senha: ").strip()

    for id_usuario, dados in usuarios.items():
        if dados["email"] == email and dados["senha"] == senha:
            print(f"\nLogin realizado com sucesso! Usuário {id_usuario} conectado.")
            return id_usuario

    print("E-mail ou senha incorretos. Encerrando o sistema.")
    exit()

def visualizar_posts():
    print("\nExibindo os posts mais recentes...")
    resposta = requests.get("https://jsonplaceholder.typicode.com/posts")
    posts = resposta.json()

    for post in posts[:5]:  
        print(f"\nPost ID: {post['id']}")
        print(f"Título: {post['title']}")
        print(f"Conteúdo: {post['body']}")
        interacoes["posts_visualizados"] += 1

    input("\nPressione Enter para voltar ao menu.")

def visualizar_comentarios():
    print("\nBuscando comentários...")
    resposta = requests.get("https://jsonplaceholder.typicode.com/comments")
    comentarios = resposta.json()

    for comentario in comentarios[:5]:
        print(f"\nComentário ID: {comentario['id']}")
        print(f"Post relacionado: {comentario['postId']}")
        print(f"Autor: {comentario['name']}")
        print(f"Comentário: {comentario['body']}")
        interacoes["comentarios_visualizados"] += 1

    input("\nPressione Enter para voltar ao menu.")


def visualizar_meus_posts(user_id):
    print("\nExibindo seus próprios posts...")
    resposta = requests.get(f"https://jsonplaceholder.typicode.com/posts?userId={user_id}")
    posts = resposta.json()

    for post in posts:
        print(f"\nPost ID: {post['id']}")
        print(f"Título: {post['title']}")
        print(f"Conteúdo: {post['body']}")
        interacoes["posts_visualizados"] += 1

    input("\nPressione Enter para voltar ao menu.")

def filtrar_posts_por_usuario():
    try:
        outro_id = int(input("Digite o ID de outro usuário (1 a 10): "))
        resposta = requests.get(f"https://jsonplaceholder.typicode.com/posts?userId={outro_id}")
        posts = resposta.json()

        if not posts:
            print("Nenhum post encontrado para esse usuário.")
            return

        print(f"\nExibindo posts do usuário {outro_id}:")

        for post in posts[:5]:
            print(f"\nPost ID: {post['id']}")
            print(f"Título: {post['title']}")
            print(f"Conteúdo: {post['body']}")
            interacoes["posts_visualizados"] += 1

    except ValueError:
        print("ID inválido. Digite um número inteiro.")
    input("\nPressione Enter para voltar ao menu.")

def criar_post(user_id):
    print("\nVamos criar um novo post.")
    titulo = input("Título do post: ")
    corpo = input("Conteúdo do post: ")

    dados_post = {
        "title": titulo,
        "body": corpo,
        "userId": user_id
    }

    resposta = requests.post("https://jsonplaceholder.typicode.com/posts", json=dados_post)

    if resposta.status_code == 201:
        print("Post criado com sucesso (simulação via API).")
        interacoes["posts_criados"] += 1
    else:
        print("Houve um erro ao criar o post.")

    input("\nPressione Enter para voltar ao menu.")


def exibir_resumo():
    print("\nRESUMO DAS SUAS INTERAÇÕES:")
    print(f"- Posts visualizados: {interacoes['posts_visualizados']}")
    print(f"- Comentários visualizados: {interacoes['comentarios_visualizados']}")
    print(f"- Posts criados: {interacoes['posts_criados']}")
    print("Obrigado por usar o sistema. Até a próxima!")

def menu():
    usuario_logado = login()

    while True:
        print("\n===== MENU PRINCIPAL =====")
        print("1. Visualizar posts públicos")
        print("2. Ver comentários")
        print("3. Ver meus posts")
        print("4. Ver posts de outro usuário")
        print("5. Criar um novo post")
        print("6. Sair do sistema")
        print("==========================")

        opcao = input("Escolha uma opção (1 a 6): ").strip()

        if opcao == "1":
            visualizar_posts()
        elif opcao == "2":
            visualizar_comentarios()
        elif opcao == "3":
            visualizar_meus_posts(usuario_logado)
        elif opcao == "4":
            filtrar_posts_por_usuario()
        elif opcao == "5":
            criar_post(usuario_logado)
        elif opcao == "6":
            exibir_resumo()
            break
        else:
            print("Opção inválida. Por favor, escolha um número de 1 a 6.")

if __name__ == "__main__":
    menu()
