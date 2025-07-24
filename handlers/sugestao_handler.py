from telegram import Update
from telegram.ext import ContextTypes
from service.prediction_service import get_predictions

async def sugestao_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    predictions = get_predictions()
    if not predictions:
        await update.message.reply_text("Nenhuma sugestão disponível agora.")
        return
    response = "💡 *Sugestões de Apostas:*\n\n"
    for p in predictions:
        response += f"{p['match']}: {p['tip']} (Odds: {p['odds']})\n"
    await update.message.reply_text(response, parse_mode="Markdown")