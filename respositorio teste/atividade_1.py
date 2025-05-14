import requests
import os

api_key = "3d07521cf5c347aebd75b5e68ed39259"
if not api_key:
    raise ValueError("API Key não encontrada no arquivo .env.")

headers = {
    'X-Api-Key': api_key
}

url = "https://newsapi.org/v2/everything"

historico_temas = []
total_noticias = 0

def menu():
    print("\n=== MENU ===")
    print("1 - Buscar notícias por tema")
    print("0 - Sair")
    return input("Escolha uma opção: ")

def buscar_noticias():
    global total_noticias

    tema = input("\nDigite o tema que deseja buscar: ").strip()
    if not tema:
        print("Tema inválido. Tente novamente.")
        return

    try:
        qtd = int(input("Quantas notícias deseja buscar? (1 a 10): "))
        if qtd < 1 or qtd > 10:
            print("Número inválido. Permitido entre 1 e 10.")
            return
    except ValueError:
        print("Entrada inválida. Digite um número.")
        return

    params = {
        'q': tema,
        'pageSize': qtd,
        'language': 'pt',
        'sortBy': 'publishedAt'
    }

    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        dados = response.json()
        artigos = dados.get('articles', [])

        if not artigos:
            print("Nenhuma notícia encontrada para o tema.")
            return

        print(f"\n{len(artigos)} notícias encontradas sobre '{tema}':")
        for i, artigo in enumerate(artigos, start=1):
            titulo = artigo.get('title','Sem título')
            fonte = artigo.get('source',{}).get('name', 'Fonte desconhecida')
            autor = artigo.get('author') or 'Autor não informado'

            print(f"\n{i}. {titulo}")
            print(f"Fonte: {fonte}")
            print(f"Autor: {autor}")

        historico_temas.append(tema)
        total_noticias += len(artigos)
    else:
        print(f"Erro na requisição: {response.status_code}")

def mostrar_resumo():
    print("\n=== RESUMO DA SESSÃO ===")
    print(f"Total de notícias exibidas: {total_noticias}")
    if historico_temas:
        print("Temas buscados:")
        for i, tema in enumerate(historico_temas, start=1):
            print(f"{i}. {tema}")
    else:
        print("Nenhum tema foi buscado.")

while True:
    opcao = menu()

    if opcao == '0':
        print("\nSaindo...")
        mostrar_resumo()
        break
    elif opcao == '1':
        buscar_noticias()
    else:
        print("Opção inválida. Tente novamente.")