from telegram import Update
from telegram.ext import ContextTypes
from service.flashscore_scraper import coletar_jogos_do_dia

async def hoje_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    jogos = obter_jogos_do_dia()

    if not jogos:
        await update.message.reply_text("Não há jogos marcados para hoje.")
        return

    mensagem = "\ud83c\udf1f *Jogos de Hoje:*\n\n"
    for jogo in jogos:
        mensagem += f"{jogo['time_casa']} x {jogo['time_fora']}\n"
    await update.message.reply_text(mensagem, parse_mode="Markdown")
