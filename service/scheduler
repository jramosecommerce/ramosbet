from apscheduler.schedulers.background import BackgroundScheduler
from service.prediction_service import gerar_sugestoes_dia

def iniciar_scheduler(bot):
    scheduler = BackgroundScheduler()

    def enviar_sugestoes():
        sugestoes = gerar_sugestoes_dia()
        for texto in sugestoes:
            bot.send_message(chat_id=SEU_CHAT_ID, text=texto, parse_mode="Markdown")

    scheduler.add_job(enviar_sugestoes, trigger='cron', hour=10)  # Altere o horário conforme preferir
    scheduler.start()
