from telegram import Update
from telegram.ext import CallbackContext
from service.flashscore_scraper import get_games_today

def estatisticas(update: Update, context: CallbackContext):
    games = get_games_today(strategy="favorites")

    if not games:
        update.message.reply_text("⚠️ Não foi possível obter estatísticas.")
        return

    message = "📊 *Estatísticas simuladas dos jogos:*\n\n"
    for game in games[:5]:  # Simula para 5 jogos
        message += f"📌 {game['home']} x {game['away']}\n"
        message += f"📈 Chutes: {game['home']}: {5 + len(game['home'])}, {game['away']}: {4 + len(game['away'])}\n"
        message += f"🎯 Finalizações certas: {game['home']}: 3, {game['away']}: 2\n"
        message += f"🟨 Cartões estimados: {game['home']}: 1, {game['away']}: 2\n\n"

    update.message.reply_text(message, parse_mode="Markdown")