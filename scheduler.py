from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

def start_scheduler(app, callback):
    scheduler = BackgroundScheduler()
    scheduler.add_job(
        callback,
        trigger=CronTrigger(hour=14, minute=0),
        args=[app],
    )
    scheduler.start()