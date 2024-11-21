import requests
from bs4 import BeautifulSoup
import time
import csv

# Função para extrair o link de todos os manhwas da página especificada
def get_manhwa_links(base_url):
    response = requests.get(base_url)
    
    # Verificando se a resposta foi bem sucedida
    if response.status_code != 200:
        print(f"Falha ao acessar {base_url}. Código de status: {response.status_code}")
        return []
    
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Procurando todos os links dos manhwas na página atual
    loop_content = soup.find('div', {'id': 'loop-content', 'class': 'page-content-listing item-big_thumbnail'})
    if loop_content:
        manhwa_links = [a['href'] for a in loop_content.find_all('a', href=True) if a.parent.name == 'h3']
        return manhwa_links
    return []

# Função para extrair informações do manhwa a partir da URL
def extract_manhwa_details(url):
    response = requests.get(url)
    
    # Verificando se a resposta foi bem sucedida
    if response.status_code != 200:
        print(f"Falha ao acessar {url}. Código de status: {response.status_code}")
        return None
    
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Extraindo as informações principais
    try:
        title = soup.find('span', class_='rate-title').text.strip()
    except AttributeError:
        title = 'N/A'
    
    try:
        rating = soup.find('div', class_='post-rating').find('span', class_='score').text.strip()
    except AttributeError:
        rating = 'N/A'
    
    try:
        alternative = soup.find('div', class_='summary-content').text.strip()
    except AttributeError:
        alternative = 'N/A'
    
    try:
        author = soup.find('div', class_='author-content').text.strip()
    except AttributeError:
        author = 'N/A'
    
    try:
        artist = soup.find('div', class_='artist-content').text.strip()
    except AttributeError:
        artist = 'N/A'
    
    try:
        genres = [genre.text.strip() for genre in soup.find('div', class_='genres-content').find_all('a')]
    except AttributeError:
        genres = []

    try:
        release_year = soup.find('div', class_='post-content_item').find('a').text.strip()
    except AttributeError:
        release_year = 'N/A'
    
    try:
        status = soup.find('div', class_='post-status').find('div', class_='summary-content').text.strip()
    except AttributeError:
        status = 'N/A'
    
    try:
        comments = soup.find('div', class_='count-comment').find('span', class_='disqus-comment-count').text.strip()
    except AttributeError:
        comments = 'N/A'
    
    # Retornando as informações como um dicionário
    return {
        "Title": title,
        "Rating": rating,
        "Alternative Titles": alternative,
        "Author": author,
        "Artist": artist,
        "Genres": ', '.join(genres),
        "Release Year": release_year,
        "Status": status,
        "Comments": comments
    }

# Nome do arquivo CSV
csv_filename = "manhwas.csv"

# Cabeçalho do CSV
csv_headers = ["Title", "Rating", "Alternative Titles", "Author", "Artist", "Genres", "Release Year", "Status", "Comments"]

# Criando o arquivo CSV e adicionando o cabeçalho
with open(csv_filename, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=csv_headers)
    writer.writeheader()

    # Buscando as primeiras 5 páginas
    for page in range(1, 6):
        page_url = f"https://flowermanga.net/page/{page}/"
        print(f"Buscando manhwas na página {page}...")
        
        # Adicionando um tempo de espera para evitar bloqueio por muitas requisições seguidas
        time.sleep(3)
        
        manhwa_links = get_manhwa_links(page_url)
        
        # Extraindo informações de cada manhwa da página e escrevendo no CSV
        for link in manhwa_links:
            manhwa_details = extract_manhwa_details(link)
            if manhwa_details:
                writer.writerow(manhwa_details)

print(f"Informações dos manhwas foram salvas em '{csv_filename}' com sucesso.")
