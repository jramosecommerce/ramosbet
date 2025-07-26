import asyncio
from telegram.ext import ApplicationBuilder
from handlers.start_handler import start
from handlers.hoje_handler import registrar_handlers_hoje
from handlers.estatisticas_handler import registrar_handlers_estatisticas
from handlers.sugestao_handler import registrar_handlers_sugestao
from telegram.ext import CommandHandler

# Substitua pelo seu token do BotFather
TOKEN = "8242348358:AAES95eDSqPFGoyZ7vmgZFolEBSClE40O_Y"

async def main():
    app = ApplicationBuilder().token(TOKEN).build()

    # /start
    app.add_handler(CommandHandler("start", start))

    # /hoje
    registrar_handlers_hoje(app)

    # /estatisticas
    registrar_handlers_estatisticas(app)

    # /sugestao
    registrar_handlers_sugestao(app)

    print("✅ Bot está rodando...")
    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
