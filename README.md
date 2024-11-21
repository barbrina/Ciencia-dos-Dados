# Web Scraping Projects

## Atividade 1: Web Scraping no Site Sucupira da CAPES

Nesta atividade, foi criado um script em Python para realizar web scraping no site Sucupira da CAPES. O objetivo era extrair informações sobre programas de pós-graduação em várias universidades e salvar essas informações em arquivos CSV.

### Passos Seguidos:
1. **Obtenção de URLs**: Foram coletadas todas as URLs dos programas de pós-graduação listados nas primeiras 25 páginas do site Sucupira, com 20 programas por página, totalizando aproximadamente 500 programas.
2. **Coleta de Informações Específicas**: Acessamos cada página individual dos programas para coletar informações como nome da universidade, código do curso, área de avaliação, área básica, situação do programa, nota, detalhes sobre mestrado e doutorado, e informações sobre CEP e cidade da instituição.
3. **Armazenamento dos Dados**: Os dados foram armazenados em dois arquivos CSV: um contendo os links dos programas ("Universidade" e "Link do Programa") e outro com os detalhes dos programas ("universidade", "codigo", "area_avaliacao", "area_basica", etc.).

### Tecnologias Utilizadas:
- **Selenium**: Automação do navegador e extração dos dados.
- **csv**: Armazenamento dos dados extraídos.
- **time**: Pausas para evitar erros durante o carregamento das páginas.

## Atividade 2: Web Scraping de Sites de Manhwas e Filmes

### 1. Web Scraping no Site Flowermanga.net
Nesta atividade, foi criado um script em Python para extrair informações detalhadas dos manhwas listados nas primeiras 5 páginas do site flowermanga.net e salvar em um arquivo CSV.

### Passos Seguidos:
1. **Obtenção de URLs**: Foram coletadas todas as URLs dos manhwas nas páginas 1 a 5.
2. **Coleta de Informações**: Extraímos informações como título, autor, artista, gênero, classificação, etc.
3. **Armazenamento dos Dados**: Os dados foram armazenados em um arquivo CSV (manhwas.csv).

### Tecnologias Utilizadas:
- **requests**: Requisições HTTP.
- **BeautifulSoup**: Parseamento de HTML.
- **csv**: Armazenamento dos dados.

### 2. Web Scraping no Site Rotten Tomatoes
Nesta atividade, foi criado um script em Python para extrair informações sobre filmes e séries populares do site Rotten Tomatoes e salvar em um arquivo CSV.

### Passos Seguidos:
1. **Obtenção de URLs**: Coletamos URLs dos filmes e séries populares na página inicial do site.
2. **Coleta de Informações**: Extraímos título, nota dos críticos e nota do público.
3. **Armazenamento dos Dados**: Os dados foram armazenados em um arquivo CSV (rottentomatoes_data.csv).

### Tecnologias Utilizadas:
- **Selenium**: Automação do navegador e extração dos dados.
- **csv**: Armazenamento dos dados.

## Atividade 3: Web Scraping no Site XKCD
Nesta atividade, foi criado um script em Python para realizar web scraping no site XKCD, com o objetivo de baixar todas as tirinhas disponíveis, da mais recente até a primeira.

### Passos Seguidos:
1. **Carregamento da Página Inicial**: Carregamos a página inicial do XKCD (http://xkcd.com) para acessar a tirinha mais recente.
2. **Extração da URL da Imagem**: Utilizamos o BeautifulSoup para analisar o HTML e identificar o elemento contendo a URL da tirinha, que foi então baixada.
3. **Armazenamento da Imagem**: As imagens foram salvas na pasta `xkcd_comics`.
4. **Navegação para Tirinha Anterior**: Localizamos o link "Previous Comic" para navegar e repetir o processo até a primeira tirinha.

### Tecnologias Utilizadas:
- **requests**: Download das páginas e imagens.
- **BeautifulSoup**: Análise do HTML.
- **os**: Manipulação de diretórios e arquivos.

