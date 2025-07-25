from telegram import Update
from telegram.ext import ContextTypes
from service.flashscore_scraper import coletar_jogos_do_dia
from service.prediction_service import gerar_sugestao

async def sugestao_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    jogos = coletar_jogos_do_dia()
    if not jogos:
        await update.message.reply_text("Sem sugestões para hoje.")
        return

    mensagem = "\ud83d\udce2 *Sugestões de Apostas:*\n\n"
    for jogo in jogos[:5]:
        mensagem += gerar_sugestao(jogo)
    await update.message.reply_text(mensagem, parse_mode="Markdown")
