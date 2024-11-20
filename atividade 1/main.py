# -*- coding: utf-8 -*-
import re
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException, ElementClickInterceptedException
import time

# Configuração do Selenium
chrome_options = Options()
chrome_options.add_argument("--headless")  # Rodar sem abrir o navegador
service = Service('chromedriver.exe')
driver = webdriver.Chrome(service=service, options=chrome_options)

# Lista para armazenar os links de detalhes de cada programa
programa_links = []

# Loop para percorrer as 25 páginas
for page in range(0, 26):
    # URL da página principal com o parâmetro da página ajustado
    url_principal = f"https://sucupira.capes.gov.br/programas?search=&size=20&page={page}"
    driver.get(url_principal)

    # Esperar a página carregar
    time.sleep(3)

    # Capturar links dos programas na página atual
    programas = driver.find_elements(By.XPATH, "//a[contains(@href, '/programas/detalhamento')]")
    for programa in programas:
        link_programa = programa.get_attribute("href")
        programa_links.append(link_programa)

    print(f"Total de links coletados na página {page + 1}: {len(programa_links)}")

# Salvar os links em um arquivo CSV
with open('links_programas.csv', mode='w', newline='', encoding='utf-8-sig') as file:
    writer = csv.writer(file, delimiter=';')
    writer.writerow(['Universidade', 'Link do Programa'])
    for programa in programas:
        universidade = programa.text
        link_programa = programa.get_attribute("href")
        writer.writerow([universidade, link_programa])

print(f"Total de links coletados ao final de 25 páginas: {len(programa_links)}")


# Função para extrair informações de um programa
def extrair_informacoes(link):
    try:
        driver.get(link)
        time.sleep(1)  # Esperar a página carregar
        print(f"Processando o link: {link}")

        # Universidade
        try:
            universidade = driver.find_element(By.XPATH, "//div[contains(@class, 'item-lista')]//span").text
        except NoSuchElementException:
            universidade = "Não disponível"

        # Código do curso
        try:
            codigo = driver.find_element(By.XPATH, "//div[@class='q-item__label']/span").text
        except NoSuchElementException:
            codigo = "Não disponível"

        # Área de avaliação
        try:
            area_avaliacao = driver.find_element(
                By.XPATH, "//div[contains(@class, 'q-item__label--header') and contains(text(), 'Área de avaliação')]"
            ).find_element(By.XPATH, "./following::span[1]").text
        except NoSuchElementException:
            area_avaliacao = "Não disponível"

        # Área básica
        try:
            area_basica = driver.find_element(
                By.XPATH, "//div[contains(@class, 'q-item__label--header') and contains(text(), 'Área básica')]"
            ).find_element(By.XPATH, "./following::span[1]").text
        except NoSuchElementException:
            area_basica = "Não disponível"

        # Situação
        try:
            situacao = driver.find_element(
                By.XPATH, "//div[contains(@class, 'q-item__label--header') and contains(text(), 'Situação')]"
            ).find_element(By.XPATH, "./following::span[1]").text
        except NoSuchElementException:
            situacao = "Não disponível"

        # Nota
        try:
            nota = driver.find_element(By.XPATH, "//div[contains(@class, 'q-badge')]").text.replace("Nota ", "").strip()
        except NoSuchElementException:
            nota = "Não disponível"

         # Mestrado e Doutorado
        try:
            botoes_expandir = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.XPATH, "//i[contains(@class, 'mdi-plus')]"))
            )
            for botao in botoes_expandir:
                try:
                    botao.click()
                    time.sleep(1)
                except ElementClickInterceptedException:
                    # Tentar clicar usando ActionChains caso o clique direto falhe
                    from selenium.webdriver.common.action_chains import ActionChains
                    ActionChains(driver).move_to_element(botao).click().perform()
        except TimeoutException:
            print("Botoes de expansão não encontrados ou não clicáveis.")

        # Informações do Mestrado
        mestrado_presente = False
        try:
            if driver.find_element(By.XPATH, "//h6[contains(text(), '| Mestrado')]"):
                mestrado_presente = True
        except NoSuchElementException:
            mestrado_presente = False

        if mestrado_presente:
            try:
                nota_mestrado = driver.find_element(By.XPATH, "(//div[contains(@class, 'item-lista')])[8]").text
                situacao_mestrado = driver.find_element(By.XPATH, "(//div[contains(@class, 'item-lista')])[12]").text
                codigo_mestrado = driver.find_element(By.XPATH, "(//div[contains(@class, 'item-lista')])[9]").text
            except NoSuchElementException:
                nota_mestrado = situacao_mestrado = codigo_mestrado = "Não disponível"
        else:
            nota_mestrado = situacao_mestrado = codigo_mestrado = "Não disponível"

        # Informações do Doutorado
        doutorado_presente = False
        try:
            if driver.find_element(By.XPATH, "//h6[contains(text(), '| Doutorado')]"):
                doutorado_presente = True
        except NoSuchElementException:
            doutorado_presente = False

        if doutorado_presente:
            try:
                nota_doutorado = driver.find_element(By.XPATH, "(//div[contains(@class, 'item-lista')])[17]").text
                situacao_doutorado = driver.find_element(By.XPATH, "(//div[contains(@class, 'item-lista')])[12]").text
                codigo_doutorado = driver.find_element(By.XPATH, "(//div[contains(@class, 'item-lista')])[18]").text
            except NoSuchElementException:
                nota_doutorado = situacao_doutorado = codigo_doutorado = "Não disponível"
        else:
            nota_doutorado = situacao_doutorado = codigo_doutorado = "Não disponível"

            
            
        # Informaçoes CEP e Cidade
        instituicoes_section = driver.find_element(By.XPATH, "//strong[text()='Instituições de ensino superior envolvidas']/ancestor::div[@class='q-card shadow-1 bg-cinza0']")
        universidade_link_elemento = instituicoes_section.find_element(By.XPATH, ".//a[contains(@href, '/programas/detalhamento')]")
        universidade_link = universidade_link_elemento.get_attribute("href")
        driver.get(universidade_link)
        time.sleep(1)  # Aguarde carregar
        driver.get(universidade_link)  # Use diretamente o link capturado
        time.sleep(1)  # Aguarde carregar
        try:
            endereco_section = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'q-item__label--header') and contains(text(), 'Endereço (Sede)')]/following-sibling::div"))
            )
            endereco_completo = endereco_section.text
            match = re.search(r"CEP\s(\d{8})\s-\s(.+?)\s-\s", endereco_completo)
            if match:
                cep = match.group(1)  # Captura o CEP
                cidade = match.group(2)  # Captura o nome da cidade
            else:
                print("CEP e Cidade não encontrados no endereço fornecido.")
        except Exception as e:
            print(f"Erro ao capturar o CEP e a Cidade: {e}")

        # Retornar dados
        return {
            "universidade": universidade,
            "codigo": codigo,
            "area_avaliacao": area_avaliacao,
            "area_basica": area_basica,
            "situacao": situacao,
            "nota": nota,
            "nota_mestrado": nota_mestrado,
            "situacao_mestrado": situacao_mestrado,
            "codigo_mestrado": codigo_mestrado,
            "nota_doutorado": nota_doutorado,
            "situacao_doutorado": situacao_doutorado,
            "codigo_doutorado": codigo_doutorado,
            "cep": cep,
            "cidade": cidade,
        }
    except Exception as e:
        print(f"Erro ao processar o link {link}: {e}")
        return None

# Extrair detalhes de cada programa
dados_detalhados = []
for link in programa_links:
    dados = extrair_informacoes(link)
    if dados:
        dados_detalhados.append(dados)

# Fechar o navegador
driver.quit()

# Salvar os detalhes dos programas em um arquivo CSV
with open('detalhes_programas.csv', mode='w', newline='', encoding='utf-8-sig') as file:
    fieldnames = [
        "universidade", "codigo", "area_avaliacao", "area_basica", "situacao",
        "nota", "nota_mestrado", "situacao_mestrado", "codigo_mestrado",
        "nota_doutorado", "situacao_doutorado", "codigo_doutorado", "cep", "cidade"
    ]
    writer = csv.DictWriter(file, fieldnames=fieldnames, delimiter=';')
    writer.writeheader()
    for dados in dados_detalhados:
        writer.writerow(dados)

print(f"Total de programas processados na primeira página: {len(dados_detalhados)}")
for programa in dados_detalhados:
    print(programa)
