# service/flashscore_scraper.py

import aiohttp
from bs4 import BeautifulSoup

BASE_URL = "https://www.flashscore.com.br/"

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

async def obter_jogos_do_dia():
    async with aiohttp.ClientSession(headers=HEADERS) as session:
        async with session.get(BASE_URL) as resp:
            html = await resp.text()

    soup = BeautifulSoup(html, "lxml")
    jogos = []

    partidas = soup.select("div.event__match")

    for partida in partidas[:10]:
        time_casa = partida.get("data-event-home")
        time_fora = partida.get("data-event-away")
        event_id = partida.get("id")

        if time_casa and time_fora and event_id:
            codigo = event_id.replace("g_", "")
            url = f"https://www.flashscore.com.br/jogo/{codigo}/#/resumo-de-jogo/estatisticas"
            jogos.append({
                "time_casa": time_casa,
                "time_fora": time_fora,
                "url_estatisticas": url,
                "codigo": codigo
            })

    return jogos


async def obter_estatisticas_reais(url_estatisticas):
    url_html = url_estatisticas.split("#")[0].replace("/#/resumo-de-jogo/estatisticas", "/estatisticas")

    async with aiohttp.ClientSession(headers=HEADERS) as session:
        async with session.get(url_html) as resp:
            html = await resp.text()

    soup = BeautifulSoup(html, "lxml")
    estatisticas = []

    linhas = soup.select(".stat__row")

    for linha in linhas:
        tipo = linha.select_one(".stat__categoryName")
        casa = linha.select_one(".stat__homeValue")
        fora = linha.select_one(".stat__awayValue")

        if tipo and casa and fora:
            estatisticas.append(f"- {tipo.text.strip()}: {casa.text.strip()} x {fora.text.strip()}")

    return estatisticas if estatisticas else ["⚠️ Estatísticas não disponíveis no momento."]


async def gerar_sugestao_aposta():
    jogos = await obter_jogos_do_dia()

    if not jogos:
        return ["⚠️ Nenhuma partida foi encontrada para hoje no Flashscore."]

    jogo = jogos[0]
    estatisticas = await obter_estatisticas_reais(jogo["url_estatisticas"])

    sugestao = (
        f"🎯 *Sugestão de Aposta para Hoje:*\n\n"
        f"🏟️ *Partida:* {jogo['time_casa']} x {jogo['time_fora']}\n"
        f"🔗 [Ver no Flashscore]({jogo['url_estatisticas']})\n\n"
        f"📊 *Estatísticas reais:*\n" +
        "\n".join(estatisticas)
    )

    return [sugestao]
