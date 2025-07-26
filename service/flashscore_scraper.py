import aiohttp
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

BASE_URL = "https://m.flashscore.com.br/"

async def obter_jogos_do_dia():
    async with aiohttp.ClientSession(headers=HEADERS) as session:
        async with session.get(BASE_URL) as resp:
            html = await resp.text()

    soup = BeautifulSoup(html, "lxml")
    jogos = []

    for evento in soup.select(".event__match"):
        casa = evento.select_one(".event__participant--home")
        fora = evento.select_one(".event__participant--away")

        if casa and fora:
            jogos.append({
                "time_casa": casa.text.strip(),
                "time_fora": fora.text.strip(),
                "url_estatisticas": BASE_URL  # ainda não temos link real de estatísticas por scraping
            })

    return jogos

async def gerar_sugestao_aposta():
    jogos = await obter_jogos_do_dia()
    if not jogos:
        return ["⚠️ Nenhuma partida foi encontrada para hoje no Flashscore (versão leve)."]

    sugestoes = []
    for jogo in jogos[:5]:
        sugestao = (
            f"🎯 *Sugestão de Aposta:*\n\n"
            f"🏟️ *Partida:* {jogo['time_casa']} x {jogo['time_fora']}\n"
            f"🔗 Acompanhe em: {BASE_URL}"
        )
        sugestoes.append(sugestao)

    return sugestoes
