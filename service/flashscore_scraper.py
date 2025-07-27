# service/flashscore_scraper.py

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

def obter_jogos_do_dia():
    opts = Options()
    opts.add_argument("--headless")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=opts)
    driver.get("https://www.flashscore.com.br/")
    driver.implicitly_wait(5)

    html = driver.page_source
    driver.quit()

    soup = BeautifulSoup(html, "lxml")
    jogos = []
    partidas = soup.select(".event__match")

    for partida in partidas[:10]:
        time_casa = partida.select_one(".event__participant--home")
        time_fora = partida.select_one(".event__participant--away")
        event_id = partida.get("id")
        if time_casa and time_fora and event_id:
            codigo = event_id.replace("g_", "")
            url = f"https://www.flashscore.com.br/jogo/{codigo}/#/resumo-de-jogo/estatisticas"
            jogos.append({
                "time_casa": time_casa.text.strip(),
                "time_fora": time_fora.text.strip(),
                "url_estatisticas": url
            })
    return jogos
