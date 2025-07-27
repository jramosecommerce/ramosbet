# service/flashscore_scraper.py

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

def obter_jogos_do_dia():
    opts = Options()
    opts.add_argument("--headless")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=opts)
    driver.get("https://www.flashscore.com.br/")
    driver.implicitly_wait(5)

    html = driver.page_source
    driver.quit()

    soup = BeautifulSoup(html, "lxml")
    jogos = []
    partidas = soup.select(".event__match")

    for partida in partidas[:10]:
        time_casa = partida.select_one(".event__participant--home")
        time_fora = partida.select_one(".event__participant--away")
        event_id = partida.get("id")
        if time_casa and time_fora and event_id:
            codigo = event_id.replace("g_", "")
            url = f"https://www.flashscore.com.br/jogo/{codigo}/#/resumo-de-jogo/estatisticas"
            jogos.append({
                "time_casa": time_casa.text.strip(),
                "time_fora": time_fora.text.strip(),
                "url_estatisticas": url
            })
    return jogos

async def obter_estatisticas_reais(nome_jogo):
    # Exemplo: nome_jogo = "15:00 - São Paulo x Palmeiras"
    nome_jogo = nome_jogo.lower()

    async with httpx.AsyncClient() as client:
        response = await client.get(FLASHCORE_URL, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")

        partidas = soup.select("div.event__match--scheduled, div.event__match--live")
        link_encontrado = None

        for partida in partidas:
            time1 = partida.select_one(".event__participant--home")
            time2 = partida.select_one(".event__participant--away")
            hora = partida.select_one(".event__time")

            if not (time1 and time2 and hora):
                continue

            texto_partida = f"{hora.text.strip()} - {time1.text.strip()} x {time2.text.strip()}".lower()

            if nome_jogo in texto_partida:
                match_id = partida.get("id", "").replace("g_1_", "")
                link_encontrado = f"{FLASHCORE_BASE}/partida/{match_id}/#/resumo-do-jogo"
                break

        if not link_encontrado:
            return f"❌ Não foi possível localizar o jogo '{nome_jogo}' no Flashscore."

        # Vai na página da partida
        response = await client.get(link_encontrado, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")

        # Exemplo de scraping simples de estatísticas
        estatisticas = []

        stats_blocks = soup.select(".stat__category")
        for bloco in stats_blocks:
            titulo = bloco.select_one(".stat__categoryName")
            valores = bloco.select(".stat__value")

            if titulo and len(valores) == 2:
                estatisticas.append(
                    f"{valores[0].text.strip()} - {titulo.text.strip()} - {valores[1].text.strip()}"
                )

        if not estatisticas:
            return f"⚠️ Estatísticas ainda não disponíveis para '{nome_jogo}'"

        resposta = f"📊 Estatísticas reais de {nome_jogo}:\n\n" + "\n".join(estatisticas)
        return resposta

async def gerar_sugestao_aposta():
    jogos = await obter_jogos_do_dia_sync()

    if not jogos:
        return "⚠️ Nenhum jogo encontrado para hoje no Flashscore."

    sugestoes = []

    for jogo in jogos[:10]:  # Limita para os 10 primeiros jogos do dia
        partes = jogo.split(" - ")
        if len(partes) < 2:
            continue

        times = partes[1]
        if " x " not in times:
            continue

        time_casa, time_fora = times.split(" x ")

        # Sugestão simples com base nos nomes dos times
        sugestao = f"📌 *{jogo}*\n" \
                   f"🔹 Sugestão: Dupla chance - {time_casa} ou empate\n" \
                   f"🔹 Possível mercado: Mais de 1.5 gols\n"

        sugestoes.append(sugestao)

    if not sugestoes:
        return "⚠️ Não foi possível gerar sugestões hoje."

    return "\n\n".join(sugestoes)

async def gerar_sugestao_aposta():
    jogos = await obter_jogos_do_dia_sync()

    if not jogos:
        return "⚠️ Nenhum jogo encontrado para hoje no Flashscore."

    sugestoes = []

    for jogo in jogos[:10]:  # Limita para os 10 primeiros jogos
        partes = jogo.split(" - ")
        if len(partes) < 2:
            continue

        times = partes[1]
        if " x " not in times:
            continue

        time_casa, time_fora = times.split(" x ")

        sugestao = f"📌 *{jogo}*\n" \
                   f"🔹 Sugestão: Dupla chance - {time_casa} ou empate\n" \
                   f"🔹 Possível mercado: Mais de 1.5 gols\n"

        sugestoes.append(sugestao)

    if not sugestoes:
        return "⚠️ Não foi possível gerar sugestões hoje."

    return "\n\n".join(sugestoes)
