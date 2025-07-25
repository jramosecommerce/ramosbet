def get_stats_fake(team):
    return {
        "posse": "55%",
        "finalizacoes": 14,
        "chutes_gol": 6,
        "escanteios": 5,
        "faltas": 10,
        "cartoes": 3
    }

def gerar_estatisticas_reais(jogo):
    return f"\n\n*{jogo['time_casa']} x {jogo['time_fora']}*\n" \
           f"Posse: {get_stats_fake(jogo['time_casa'])['posse']}\n" \
           f"Finalizações: {get_stats_fake(jogo['time_casa'])['finalizacoes']}\n" \
           f"Escanteios: {get_stats_fake(jogo['time_casa'])['escanteios']}\n" \
           f"Cartões: {get_stats_fake(jogo['time_casa'])['cartoes']}\n"
