import aiohttp
from bs4 import BeautifulSoup

BASE_URL = "https://www.flashscore.com.br"

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

async def fetch_html(url):
    async with aiohttp.ClientSession(headers=HEADERS) as session:
        async with session.get(url) as response:
            return await response.text()

async def obter_jogos_do_dia():
    html = await fetch_html(BASE_URL)
    soup = BeautifulSoup(html, "html.parser")
    jogos = []

    partidas = soup.select(".event__match")
    for partida in partidas[:10]:  # Limita para teste
        time_casa = partida.select_one(".event__participant--home").text.strip()
        time_fora = partida.select_one(".event__participant--away").text.strip()
        hora = partida.select_one(".event__time").text.strip()
        jogos.append(f"{hora} - {time_casa} x {time_fora}")

    return jogos

async def gerar_sugestao_aposta():
    html = await fetch_html(BASE_URL)
    soup = BeautifulSoup(html, "html.parser")
    partidas = soup.select(".event__match")
    sugestoes = []

    for partida in partidas[:5]:  # 5 primeiras como exemplo
        time_casa = partida.select_one(".event__participant--home").text.strip()
        time_fora = partida.select_one(".event__participant--away").text.strip()
        hora = partida.select_one(".event__time").text.strip()

        sugestao = f"⏰ {hora} - {time_casa} x {time_fora}\nSugestão: +1.5 gols ou Ambas Marcam"
        sugestoes.append(sugestao)

    return sugestoes
