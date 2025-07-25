from telegram import Update
from telegram.ext import ContextTypes
from service.flashscore_scraper import coletar_jogos_do_dia
from service.stats_service import gerar_estatisticas_reais

async def estatisticas_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    jogos = coletar_jogos_do_dia()
    if not jogos:
        await update.message.reply_text("Sem jogos encontrados.")
        return

    mensagem = "\ud83d\udcca *Estatísticas dos Jogos de Hoje:*\n"
    for jogo in jogos[:5]:  # limitar para evitar excesso de dados
        mensagem += gerar_estatisticas_reais(jogo)
    await update.message.reply_text(mensagem, parse_mode="Markdown")
