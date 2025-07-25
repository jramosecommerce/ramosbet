from telegram import Update
from telegram.ext import ContextTypes
from service.flashscore_scraper import get_today_matches

async def hoje_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    jogos = get_today_matches()
    if not jogos:
        await update.message.reply_text("⚠️ Não há jogos marcados para hoje.")
    else:
        await update.message.reply_text("\n".join(jogos))