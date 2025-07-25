import requests
from bs4 import BeautifulSoup

def get_today_matches():
    url = "https://www.flashscore.com.br/"
    response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    soup = BeautifulSoup(response.content, "html.parser")
    partidas = soup.select(".event__match")
    jogos = []
    for partida in partidas[:10]:
        time_home = partida.select_one(".event__participant--home")
        time_away = partida.select_one(".event__participant--away")
        if time_home and time_away:
            jogos.append(f"🏟️ {time_home.text} x {time_away.text}")
    return jogos