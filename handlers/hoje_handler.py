from telegram import Update
from telegram.ext import ContextTypes
from service.match_service import get_today_matches

async def hoje_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    matches = get_today_matches()
    if not matches:
        await update.message.reply_text("Não há jogos marcados para hoje.")
        return
    response = "🏟️ *Jogos de Hoje:*\n\n"
    for match in matches:
        response += f"{match['homeTeam']} x {match['awayTeam']} às {match['time']}\n"
    await update.message.reply_text(response, parse_mode="Markdown")