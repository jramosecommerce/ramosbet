from telegram import Update
from telegram.ext import CallbackContext
from service.flashscore_scraper import get_games_today

def hoje(update: Update, context: CallbackContext):
    games = get_games_today(strategy="mixed")

    if not games:
        update.message.reply_text("⚠️ Não há jogos marcados para hoje.")
        return

    message = "📅 *Jogos de Hoje:*\n\n"
    for game in games:
        message += f"🏆 {game['league']}\n"
        message += f"⚽ {game['home']} x {game['away']} às {game['time']}\n\n"

    update.message.reply_text(message, parse_mode="Markdown")