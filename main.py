from telegram import Update
from telegram.ext import (
    ApplicationBuilder, CommandHandler, CallbackQueryHandler,
    ContextTypes
)
from handlers.start_handler import start
from handlers.hoje_handler import hoje_handler
from handlers.estatisticas_handler import estatisticas_handler, handle_estatisticas_selection
from handlers.sugestao_handler import sugestao_handler
from service.scheduler import start_scheduler, scheduled_suggestion
import os

TOKEN = os.getenv("BOT_TOKEN")

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("hoje", hoje_handler))
app.add_handler(CommandHandler("estatisticas", estatisticas_handler))
app.add_handler(CallbackQueryHandler(handle_estatisticas_selection))
app.add_handler(CommandHandler("sugestao", sugestao_handler))

start_scheduler(app)

print("🤖 Bot está rodando...")
app.run_polling()
