# service/flashscore_scraper.py

import aiohttp
from bs4 import BeautifulSoup

BASE_URL = "https://www.flashscore.com.br/"

async def obter_jogos_do_dia():
    async with aiohttp.ClientSession() as session:
        async with session.get(BASE_URL) as resp:
            html = await resp.text()

    soup = BeautifulSoup(html, "lxml")
    jogos = []
    partidas = soup.select(".event__match")

    for partida in partidas[:10]:  # limita aos 10 primeiros para performance
        time_casa = partida.select_one(".event__participant--home")
        time_fora = partida.select_one(".event__participant--away")
        horario = partida.select_one(".event__time")

        if time_casa and time_fora and horario:
            jogos.append({
                "time_casa": time_casa.text.strip(),
                "time_fora": time_fora.text.strip(),
                "horario": horario.text.strip()
            })

    return jogos


async def obter_estatisticas_aleatorias():
    # Simula scraping de estatísticas por enquanto
    return (
        "📊 *Estatísticas do Jogo Selecionado:*
"
        "- Posse de bola: 52% x 48%
"
        "- Finalizações: 13 x 10
"
        "- Escanteios: 5 x 3
"
        "- Cartões: 2 x 1
"
        "- Ambos Marcam: ✅
"
        "- Mais de 2.5 Gols: ❌"
    )
