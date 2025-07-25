import requests
from bs4 import BeautifulSoup

def coletar_jogos_do_dia():
    url = "https://www.flashscore.com.br/"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    jogos = []

    for jogo in soup.select(".event__match"):
        time_casa = jogo.select_one(".event__participant--home")
        time_fora = jogo.select_one(".event__participant--away")

        if time_casa and time_fora:
            jogos.append({
                "time_casa": time_casa.text.strip(),
                "time_fora": time_fora.text.strip(),
            })

    return jogos
