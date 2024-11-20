# -*- coding: utf-8 -*-
import os
import requests
from bs4 import BeautifulSoup

def download_xkcd():
    url = 'http://xkcd.com'
    os.makedirs('images', exist_ok=True)

    while not url.endswith('#'):
        print(f'Baixando a pagina {url}...')
        res = requests.get(url)
        res.raise_for_status()

        soup = BeautifulSoup(res.text, 'html.parser')
        comic_elem = soup.select('#comic img')
        if comic_elem == []:
            print('Nao foi possivel encontrar a imagem da tirinha.')
        else:
            comic_url = 'https:' + comic_elem[0].get('src')
            # Baixa a imagem
            print(f'Baixando a imagem {comic_url}...')
            res = requests.get(comic_url)
            res.raise_for_status()
            image_file = open(os.path.join('xkcd_comics', os.path.basename(comic_url)), 'wb')
            for chunk in res.iter_content(100000):
                image_file.write(chunk)
            image_file.close()

        prev_link = soup.select('a[rel="prev"]')[0]
        url = 'http://xkcd.com' + prev_link.get('href')

    print('Todas as tirinhas foram baixadas!')

download_xkcd()
