import aiohttp
from bs4 import BeautifulSoup

BASE_URL = "https://www.flashscore.com.br/"

async def obter_jogos_do_dia():
    print("📥 Iniciando scraping dos jogos do dia...")

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(BASE_URL) as resp:
            html = await resp.text()

    soup = BeautifulSoup(html, "lxml")
    jogos = []
    partidas = soup.select(".event__match")

    print(f"✅ Total de partidas encontradas: {len(partidas)}")

    for partida in partidas[:10]:  # limita aos 10 primeiros
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

    print(f"⚽ Jogos formatados para retorno: {len(jogos)}")
    return jogos


async def obter_estatisticas_reais(url):
    print(f"🔗 Coletando estatísticas da URL: {url}")
    
    url_sem_hash = url.split("#")[0].replace("/#/resumo-de-jogo/estatisticas", "/estatisticas")
    
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(url_sem_hash) as response:
            html = await response.text()

    soup = BeautifulSoup(html, "lxml")
    estatisticas = []

    stat_rows = soup.select(".statRow")

    print(f"📊 Linhas de estatísticas encontradas: {len(stat_rows)}")

    for row in stat_rows:
        tipo = row.select_one(".statText--title")
        casa = row.select_one(".statText--home")
        fora = row.select_one(".statText--away")

        if tipo and casa and fora:
            estatisticas.append(f"- {tipo.text.strip()}: {casa.text.strip()} x {fora.text.strip()}")

    if not estatisticas:
        print("⚠️ Nenhuma estatística encontrada.")
        return ["⚠️ Estatísticas não disponíveis."]

    return estatisticas


async def gerar_sugestao_aposta():
    print("🧠 Gerando sugestão de aposta com base nas estatísticas reais...")

    jogos = await obter_jogos_do_dia()

    if not jogos:
        print("❌ Nenhum jogo encontrado.")
        return ["⚠️ Nenhuma partida foi encontrada para hoje no Flashscore."]

    jogo = jogos[0]
    print(f"🎯 Jogo escolhido: {jogo['time_casa']} x {jogo['time_fora']}")

    estatisticas = await obter_estatisticas_reais(jogo["url_estatisticas"])

    sugestao = (
        f"🎯 *Sugestão de Aposta para Hoje:*\n\n"
        f"🏟️ *Partida:* {jogo['time_casa']} x {jogo['time_fora']}\n"
        f"🔗 [Ver no Flashscore]({jogo['url_estatisticas']})\n\n"
        f"📊 *Estatísticas reais:*\n" +
        "\n".join(estatisticas)
    )

    return [sugestao]
