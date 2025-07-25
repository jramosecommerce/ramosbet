from telegram.ext import Application
from handlers.sugestao_handler import sugestao_handler
from datetime import time

def start_scheduler(app: Application):
    app.job_queue.run_daily(scheduled_suggestion, time(hour=10, minute=0))

def scheduled_suggestion(context):
    chat_id = os.getenv("GRUPO_ID")
    context.bot.send_message(chat_id=chat_id, text="Enviando sugestões automáticas...")
    context.args = []
    sugestao_handler(update=None, context=context)
