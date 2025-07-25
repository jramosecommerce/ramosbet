from telegram.ext import Updater, CommandHandler
from handlers.start_handler import start
from handlers.hoje_handler import hoje
from handlers.estatisticas_handler import estatisticas
from handlers.sugestao_handler import sugestao

import os

TOKEN = os.getenv("BOT_TOKEN")

def main():
    updater = Updater(TOKEN)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("hoje", hoje))
    dp.add_handler(CommandHandler("estatisticas", estatisticas))
    dp.add_handler(CommandHandler("sugestao", sugestao))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
