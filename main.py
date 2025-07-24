import os
from telegram.ext import ApplicationBuilder, CommandHandler
from handlers.hoje_handler import hoje_handler
from handlers.estatisticas_handler import estatisticas_handler
from handlers.sugestao_handler import sugestao_handler
from handlers.start_handler import start_handler
from scheduler import start_scheduler
from service.prediction_service import get_predictions

TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start_handler))
app.add_handler(CommandHandler("hoje", hoje_handler))
app.add_handler(CommandHandler("estatisticas", estatisticas_handler))
app.add_handler(CommandHandler("sugestao", sugestao_handler))

async def scheduled_suggestion(context):
    predictions = get_predictions()
    if not predictions:
        return
    message = "📢 *Sugestões de Apostas Automáticas:*

"
    for p in predictions:
        message += f"{p['match']}: {p['tip']} (Odds: {p['odds']})\n"
    await context.bot.send_message(chat_id=CHAT_ID, text=message, parse_mode="Markdown")

start_scheduler(app, scheduled_suggestion)

app.run_polling()