from telegram.ext import ApplicationBuilder
from handlers.hoje import registrar_handlers_hoje
from handlers.estatisticas import registrar_handlers_estatisticas
from handlers.sugestao import registrar_handlers_sugestao
import os

TOKEN = os.getenv("BOT_TOKEN")

async def main():
    app = ApplicationBuilder().token(TOKEN).build()

    registrar_handlers_hoje(app)
    registrar_handlers_estatisticas(app)
    registrar_handlers_sugestao(app)

    print("✅ Bot iniciado...")
    await app.run_polling()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
