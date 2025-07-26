from telegram import Update
from telegram.ext import CommandHandler, ContextTypes
from service.flashscore_scraper import gerar_sugestao_aposta

async def sugestao_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        await update.message.reply_text("🔍 Gerando sugestões com base nos jogos reais de hoje...")

        sugestao = await gerar_sugestao_aposta()

        if not sugestao:
            await update.message.reply_text("⚠️ Nenhuma sugestão encontrada para hoje.")
            return

        await update.message.reply_text(sugestao, parse_mode="Markdown")

    except Exception as e:
        await update.message.reply_text(f"❌ Erro ao gerar sugestão: {e}")

def registrar_handlers_sugestao(app):
    app.add_handler(CommandHandler("sugestao", sugestao_handler))
