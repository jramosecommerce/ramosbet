from telegram import Update
from telegram.ext import ContextTypes
from service.stats_service import get_past_match_stats

async def estatisticas_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    stats = get_past_match_stats("brasileirao-serie-a")
    await update.message.reply_text(stats)