from telegram.ext import Application
from datetime import time
from service.flashscore_scraper import gerar_sugestao_aposta

async def scheduled_suggestion(context):
    chat_id = context.job.context
    sugestao = await gerar_sugestao_aposta()  # Função assíncrona com dados reais
    await context.bot.send_message(chat_id=chat_id, text=sugestao, parse_mode='Markdown')

def start_scheduler(application: Application, chat_id: int):
    application.job_queue.run_daily(
        scheduled_suggestion,
        time(hour=10, minute=0),
        context=chat_id
    )
