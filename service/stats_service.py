import requests
import os

API_KEY = os.getenv("FOOTBALL_DATA_KEY")
HEADERS = {"X-Auth-Token": API_KEY}
API_URL_BASE = "https://api.football-data.org/v4/matches"

def obter_estatisticas_reais(id_partida):
    try:
        url = f"{API_URL_BASE}/{id_partida}"
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        match = response.json()

        estatisticas = f"""
📊 Estatísticas reais para *{match['homeTeam']['name']} x {match['awayTeam']['name']}*:

• Status: {match['status']}
• Gols: {match['score']['fullTime']['home']} x {match['score']['fullTime']['away']}
• Tempo: {match['score']['duration']}
"""
        return estatisticas.strip()
    except Exception as e:
        print(f"[ERRO] ao obter estatísticas: {e}")
        return "❌ Erro ao buscar estatísticas da partida."
