from telegram.ext import ApplicationBuilder, CommandHandler
from handlers.start_handler import start
from handlers.hoje_handler import hoje_handler
from handlers.estatisticas_handler import estatisticas_handler
from handlers.sugestao_handler import sugestao_handler
from service.scheduler import start_scheduler, scheduled_suggestion
import os

TOKEN = os.getenv("BOT_TOKEN")

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("hoje", hoje_handler))
app.add_handler(CommandHandler("estatisticas", estatisticas_handler))
app.add_handler(CommandHandler("sugestao", sugestao_handler))

start_scheduler(app)

print("Bot iniciado...")
app.run_polling()
