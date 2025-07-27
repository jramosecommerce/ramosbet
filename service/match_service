import requests
import os
from datetime import datetime

API_URL = "https://api.football-data.org/v4/matches"
API_KEY = os.getenv("FOOTBALL_DATA_KEY")

HEADERS = {
    "X-Auth-Token": API_KEY
}

def obter_jogos_do_dia():
    hoje = datetime.now().strftime("%Y-%m-%d")
    params = {"dateFrom": hoje, "dateTo": hoje}

    try:
        response = requests.get(API_URL, headers=HEADERS, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        jogos = []
        for match in data.get("matches", []):
            jogo = {
                "time_casa": match["homeTeam"]["name"],
                "time_fora": match["awayTeam"]["name"],
                "id_partida": match["id"]
            }
            jogos.append(jogo)

        return jogos

    except Exception as e:
        print(f"[ERRO] ao obter jogos: {e}")
        return []
