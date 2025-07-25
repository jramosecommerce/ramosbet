import asyncio
import os
import schedule
import time
from telegram import Bot
from service.prediction_service import gerar_sugestoes

def start_scheduler(app):
    async def job():
        chat_id = os.getenv("DEFAULT_CHAT_ID")
        texto = gerar_sugestoes()
        bot = Bot(token=os.getenv("TELEGRAM_TOKEN"))
        await bot.send_message(chat_id=chat_id, text=texto)

    def run_schedule():
        schedule.every().day.at("11:00").do(lambda: asyncio.run(job()))
        while True:
            schedule.run_pending()
            time.sleep(60)

    import threading
    threading.Thread(target=run_schedule, daemon=True).start()