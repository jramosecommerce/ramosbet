import aiohttp
from bs4 import BeautifulSoup

async def gerar_estatisticas_reais(url_jogo):
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    async with aiohttp.ClientSession() as session:
        async with session.get(url_jogo, headers=headers) as response:
            html = await response.text()

    soup = BeautifulSoup(html, "html.parser")

    estatisticas = {}

    estatisticas_brutas = soup.select(".stat__row")

    for stat in estatisticas_brutas:
        nome = stat.select_one(".stat__categoryName").text.strip()
        time_casa = stat.select_one(".stat__homeValue").text.strip()
        time_fora = stat.select_one(".stat__awayValue").text.strip()
        estatisticas[nome] = {
            "casa": time_casa,
            "fora": time_fora
        }

    return estatisticas
