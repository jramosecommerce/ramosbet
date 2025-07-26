import aiohttp
from bs4 import BeautifulSoup

BASE_URL = "https://www.flashscore.com.br/"

async def obter_jogos_do_dia():
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    async with aiohttp.ClientSession() as session:
        async with session.get(BASE_URL, headers=headers) as resp:
            html = await resp.text()

    soup = BeautifulSoup(html, "lxml")
    jogos = []

    # Atualizado para pegar corretamente as partidas reais
    partidas = soup.select("div[id^='g_'][data-event-home][data-event-away]")

    if not partidas:
        print("⚠️ Nenhuma tag de partida foi encontrada na página inicial do Flashscore.")

    for partida in partidas[:10]:  # limitar a 10 jogos para performance
        time_casa = partida.get("data-event-home")
        time_fora = partida.get("data-event-away")
        event_id = partida.get("id")

        if time_casa and time_fora and event_id:
            url = f"https://www.flashscore.com.br/jogo/{event_id[4:]}/#/resumo-de-jogo/estatisticas"
            jogos.append({
                "time_casa": time_casa,
                "time_fora": time_fora,
                "url_estatisticas": url
            })

    return jogos


async def obter_estatisticas_reais(url):
    url_sem_hash = url.split("#")[0].replace("/#/resumo-de-jogo/estatisticas", "/estatisticas")
    
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    async with aiohttp.ClientSession() as session:
        async with session.get(url_sem_hash, headers=headers) as response:
            html = await response.text()

    soup = BeautifulSoup(html, "lxml")
    estatisticas = []

    stat_rows = soup.select(".statRow")

    for row in stat_rows:
        tipo = row.select_one(".statText--title")
        casa = row.select_one(".statText--home")
        fora = row.select_one(".statText--away")

        if tipo and casa and fora:
            estatisticas.append(f"- {tipo.text.strip()}: {casa.text.strip()} x {fora.text.strip()}")

    return estatisticas if estatisticas else ["⚠️ Estatísticas não disponíveis."]


async def gerar_sugestao_aposta():
    jogos = await obter_jogos_do_dia()

    if not jogos:
        return ["⚠️ Nenhuma partida foi encontrada para hoje no Flashscore."]

    jogo = jogos[0]  # Pega o primeiro jogo do dia
    estatisticas = await obter_estatisticas_reais(jogo["url_estatisticas"])

    sugestao = (
        f"🎯 *Sugestão de Aposta para Hoje:*\n\n"
        f"🏟️ *Partida:* {jogo['time_casa']} x {jogo['time_fora']}\n"
        f"🔗 [Ver no Flashscore]({jogo['url_estatisticas']})\n\n"
        f"📊 *Estatísticas reais:*\n" +
        "\n".join(estatisticas)
    )

    return [sugestao]
