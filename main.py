import logging
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from handlers.start_handler import start_handler
from handlers.hoje_handler import hoje_handler
from handlers.estatisticas_handler import estatisticas_handler
from handlers.sugestao_handler import sugestao_handler

from service.scheduler import start_scheduler
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("TELEGRAM_TOKEN")

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start_handler))
app.add_handler(CommandHandler("hoje", hoje_handler))
app.add_handler(CommandHandler("estatisticas", estatisticas_handler))
app.add_handler(CommandHandler("sugestao", sugestao_handler))

start_scheduler(app)  # Inicia o agendador
print("Bot em execução...")
app.run_polling()