import requests
from bs4 import BeautifulSoup
from datetime import datetime

def obter_estatisticas_partida(url_partida):
    """ Retorna estatísticas reais da partida a partir da URL da partida no Flashscore """
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    response = requests.get(url_partida, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    estatisticas_raw = soup.select(".statRow")

    dados = {
        "times": "Desconhecido",
        "hora": "Desconhecido",
        "finalizacoes": "N/D",
        "chutes_no_gol": "N/D",
        "chutes_fora": "N/D",
        "posse": "N/D",
        "amarelos": "N/D",
        "vermelhos": "N/D",
        "escanteios": "N/D",
    }

    # Tentativa de pegar o nome dos times
    titulo = soup.select_one(".duelParticipant__name")
    if titulo:
        dados["times"] = " x ".join([t.text.strip() for t in soup.select(".duelParticipant__name")])

    # Tentativa de pegar o horário do jogo
    hora_tag = soup.select_one(".duelParticipant__startTime")
    if hora_tag:
        dados["hora"] = hora_tag.text.strip()

    for stat in estatisticas_raw:
        tipo = stat.select_one(".statText--title")
        casa = stat.select_one(".statText--home")
        fora = stat.select_one(".statText--away")

        if tipo and casa and fora:
            tipo_texto = tipo.text.strip().lower()
            valor = f"{casa.text.strip()} x {fora.text.strip()}"

            if "finalizações" in tipo_texto:
                dados["finalizacoes"] = valor
            elif "chutes no gol" in tipo_texto:
                dados["chutes_no_gol"] = valor
            elif "chutes para fora" in tipo_texto:
                dados["chutes_fora"] = valor
            elif "posse de bola" in tipo_texto:
                dados["posse"] = valor
            elif "cartões amarelos" in tipo_texto:
                dados["amarelos"] = valor
            elif "cartões vermelhos" in tipo_texto:
                dados["vermelhos"] = valor
            elif "escanteios" in tipo_texto:
                dados["escanteios"] = valor

    return dados

def listar_partidas_do_dia():
    """ Retorna uma lista de partidas com hora, times e URL """
    url = "https://www.flashscore.com.br/"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    partidas = []
    jogos = soup.select(".event__match")

    for jogo in jogos:
        time_casa = jogo.get("data-event-home")
        time_fora = jogo.get("data-event-away")
        event_id = jogo.get("id")
        hora_tag = jogo.select_one(".event__time")

        if time_casa and time_fora and event_id:
            link = f"https://www.flashscore.com.br/jogo/{event_id[4:]}/#/resumo-de-jogo/estatisticas"
            nome = f"{time_casa} x {time_fora}"
            hora = hora_tag.text.strip() if hora_tag else "??:??"
            partidas.append({
                "times": nome,
                "hora": hora,
                "url": link
            })

    return partidas
