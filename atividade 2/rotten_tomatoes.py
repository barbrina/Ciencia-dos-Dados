# -*- coding: utf-8 -*-
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
csv_filename = "rottentomatoes_data.csv"
header = ['Tipo', 'Titulo', 'Nota dos Criticos', 'Nota do Publico']

with open(csv_filename, mode='w', newline='', encoding='utf-8') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(header) 

    try:
        driver.get("https://www.rottentomatoes.com/")
        wait = WebDriverWait(driver, 10)

        # -----------------
        # Extrair dados dos filmes populares
        # -----------------
        try:
            popular_movies_section = wait.until(EC.presence_of_element_located((By.XPATH, "//section[contains(@class, 'dynamic-text-list')]//h2[text()='Popular Streaming Movies']/following-sibling::ul[@slot='list-items']")))
            movie_links = popular_movies_section.find_elements(By.TAG_NAME, 'a')
            movie_urls = set([link.get_attribute('href') for link in movie_links if '/m/' in link.get_attribute('href')])
            for url in movie_urls:
                driver.get(url)
                try:
                    movie_title = wait.until(EC.presence_of_element_located((By.TAG_NAME, 'h1'))).text
                    try:
                        critics_score_element = wait.until(EC.presence_of_element_located((By.XPATH, "//rt-text[@slot='criticsScore']")))
                        critics_score = critics_score_element.text
                    except:
                        critics_score = "Nao disponivel"
                    try:
                        audience_score_element = wait.until(EC.presence_of_element_located((By.XPATH, "//rt-text[@slot='audienceScore']")))
                        audience_score = audience_score_element.text
                    except:
                        audience_score = "Nao disponivel"
                    writer.writerow(['Filme', movie_title, critics_score, audience_score])

                    print(f"Filme: {movie_title}, Nota dos Criticos: {critics_score}, Nota do Publico: {audience_score}")

                except Exception as e:
                    print(f"Nao foi possivel coletar as informacoes do filme em {url}. Erro: {e}")
                
                driver.back()
                time.sleep(3) 

        except Exception as e:
            print(f"Nao foi possivel coletar informacoes dos filmes populares. Erro: {e}")

        # -----------------
        # Extrair dados das séries de TV populares
        # -----------------
        try:
            popular_tv_section = wait.until(EC.presence_of_element_located((By.XPATH, "//section[contains(@class, 'dynamic-text-list')]//h2[text()='Popular TV ']/following-sibling::ul[@slot='list-items']")))
            tv_links = popular_tv_section.find_elements(By.TAG_NAME, 'a')
            tv_urls = set([link.get_attribute('href') for link in tv_links if '/tv/' in link.get_attribute('href')])

            for url in tv_urls:
                driver.get(url)
                try:
                    tv_title = wait.until(EC.presence_of_element_located((By.TAG_NAME, 'h1'))).text
                    try:
                        critics_score_element = wait.until(EC.presence_of_element_located((By.XPATH, "//rt-text[@slot='criticsScore']")))
                        critics_score = critics_score_element.text
                    except:
                        critics_score = "Nao disponivel"
                    try:
                        audience_score_element = wait.until(EC.presence_of_element_located((By.XPATH, "//rt-text[@slot='audienceScore']")))
                        audience_score = audience_score_element.text
                    except:
                        audience_score = "Nao disponivel"

                    writer.writerow(['Serie de TV', tv_title, critics_score, audience_score])

                    print(f"Serie de TV: {tv_title}, Nota dos Criticos: {critics_score}, Nota do Publico: {audience_score}")

                except Exception as e:
                    print(f"Nao foi possivel coletar as informacoes da serie de TV em {url}. Erro: {e}")
                
                driver.back()
                time.sleep(3) 

        except Exception as e:
            print(f"Nao foi possivel coletar informacoes das series de TV populares. Erro: {e}")

    except Exception as e:
        print(f"Ocorreu um erro geral: {e}")

    finally:
        # Feche o navegador
        driver.quit()
