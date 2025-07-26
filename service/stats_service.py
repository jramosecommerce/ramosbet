service/stats_service.py

import requests from bs4 import BeautifulSoup from datetime import datetime

def obter_estatisticas_partida(url_partida): """ Retorna estatísticas reais da partida a partir da URL da partida no Flashscore """ headers = { "User-Agent": "Mozilla/5.0" } response = requests.get(url_partida, headers=headers) soup = BeautifulSoup(response.text, "html.parser")

estatisticas = []

estatisticas_raw = soup.select(".statRow")
for stat in estatisticas_raw:
    tipo = stat.select_one(".statText--title")
    casa = stat.select_one(".statText--home")
    fora = stat.select_one(".statText--away")

    if tipo and casa and fora:
        estatisticas.append(f"{tipo.text.strip()}: {casa.text.strip()} x {fora.text.strip()}")

return "\n".join(estatisticas) if estatisticas else "Estatísticas não encontradas para essa partida."

def listar_partidas_do_dia(): """ Retorna uma lista de partidas com nome e URL para estatísticas """ url = "https://www.flashscore.com.br/" headers = {"User-Agent": "Mozilla/5.0"} response = requests.get(url, headers=headers) soup = BeautifulSoup(response.text, "html.parser")

partidas = []
jogos = soup.select(".event__match")
for jogo in jogos:
    time_casa = jogo.get("data-event-home")
    time_fora = jogo.get("data-event-away")
    event_id = jogo.get("id")
    if time_casa and time_fora and event_id:
        link = f"https://www.flashscore.com.br/jogo/{event_id[4:]}/#/resumo-de-jogo/estatisticas"
        nome = f"{time_casa} x {time_fora}"
        partidas.append({"nome": nome, "url": link})

return partidas

