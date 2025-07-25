import aiohttp
from bs4 import BeautifulSoup

async def get_past_match_stats(team_name):
    url = f"https://www.flashscore.com.br/equipe/{team_name}/resultados/"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            html = await response.text()

    soup = BeautifulSoup(html, "html.parser")

    resultados = []
    partidas = soup.select(".event__match--static")[:5]  # últimos 5 jogos

    for partida in partidas:
        data = partida.select_one(".event__time").text.strip()
        casa = partida.select_one(".event__participant--home").text.strip()
        fora = partida.select_one(".event__participant--away").text.strip()
        placar_casa = partida.select_one(".event__score--home").text.strip()
        placar_fora = partida.select_one(".event__score--away").text.strip()

        resultados.append({
            "data": data,
            "time_casa": casa,
            "time_fora": fora,
            "placar": f"{placar_casa} x {placar_fora}"
        })

    return resultados
