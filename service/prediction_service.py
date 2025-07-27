from .match_service import obter_jogos_do_dia
from .stats_service import obter_estatisticas_reais

def gerar_sugestao_aposta(id_partida, nome_jogo):
    # Sugestões básicas simuladas (você pode aprimorar com mais dados)
    sugestao = f"""
🎯 Sugestão de Aposta para *{nome_jogo}*:

🏆 *Dupla Hipótese*: {nome_jogo.split(' x ')[0]} ou Empate  
⚽ *Mais de 1.5 gols*  
📈 *Ambos marcam*: Sim
"""
    return sugestao.strip()

def gerar_sugestoes_dia():
    sugestoes = []
    jogos = obter_jogos_do_dia()

    for jogo in jogos:
        try:
            nome_jogo = f"{jogo['time_casa']} x {jogo['time_fora']}"
            texto = gerar_sugestao_aposta(jogo["id_partida"], nome_jogo)
            if texto:
                sugestoes.append(texto)
        except Exception as e:
            print(f"[ERRO] em sugestão: {e}")

    return sugestoes
