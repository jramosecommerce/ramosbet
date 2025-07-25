from telegram import Update
from telegram.ext import CallbackContext
from service.flashscore_scraper import get_games_today

def sugestao(update: Update, context: CallbackContext):
    games = get_games_today(strategy="favorites")

    if not games:
        update.message.reply_text("⚠️ Nenhuma sugestão disponível no momento.")
        return

    message = "💡 *Sugestões de apostas para hoje:*\n\n"
    for game in games[:5]:  # Sugestões para 5 jogos
        message += f"⚽ {game['home']} x {game['away']}\n"
        message += f"✅ Sugestão: Dupla hipótese - {game['home']} ou empate\n"
        message += f"📊 Mais de 1.5 gols na partida\n\n"

    update.message.reply_text(message, parse_mode="Markdown")