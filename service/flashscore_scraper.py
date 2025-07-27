import requests
from bs4 import BeautifulSoup
from datetime import datetime

FLASHCORE_URL = "https://www.flashscore.com.br/"  # versão leve, ideal para scraping

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

def obter_jogos_do_dia():
    try:
        response = requests.get(FLASHCORE_URL, headers=HEADERS, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        jogos = []
        eventos = soup.select(".event__match")

        for evento in eventos:
            time_a = evento.select_one(".event__participant--home")
            time_b = evento.select_one(".event__participant--away")
            horario = evento.get("data-start-time")

            if time_a and time_b:
                nome_jogo = f"{time_a.text.strip()} x {time_b.text.strip()}"
                hora = datetime.fromtimestamp(int(horario)).strftime("%H:%M") if horario else "Horário desconhecido"
                jogos.append(f"{nome_jogo} - {hora}")

        return jogos if jogos else ["⚠️ Nenhum jogo encontrado."]
    except Exception as e:
        return [f"❌ Erro ao obter jogos: {str(e)}"]

def obter_estatisticas_reais(jogo_nome):
    # Exemplo estático – você pode adaptar com scraping real de estatísticas por URL
    estatisticas = f"""
📊 Estatísticas reais para *{jogo_nome}*:

• Finalizações: 12 x 9  
• Chutes no gol: 6 x 3  
• Escanteios: 5 x 7  
• Cartões: 🟨 2 x 3 | 🟥 0 x 1  
• Ambos Marcam: ✅  
• Total de Gols: Mais de 2.5 ✅  
"""
    return estatisticas

def gerar_sugestao_aposta(jogo_nome):
    # Geração simples baseada em "estatística genérica"
    sugestao = f"""
🎯 Sugestão de Aposta para *{jogo_nome}*:

🏆 *Dupla Hipótese*: {jogo_nome.split(' x ')[0]} ou Empate  
⚽ *Mais de 1.5 gols*  
📈 *Ambos marcam*: Sim  
"""
    return sugestao

def gerar_sugestoes_dia():
    jogos = obter_jogos_do_dia()  # Deve retornar lista com nomes dos jogos
    sugestoes = []

    for jogo in jogos:
        try:
            texto = gerar_sugestao_aposta(jogo_nome=jogo)
            if texto:
                sugestoes.append(texto)
        except Exception as e:
            print(f"[ERRO] Não foi possível gerar sugestão para {jogo}: {e}")

    return sugestoes
