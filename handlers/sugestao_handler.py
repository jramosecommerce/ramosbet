from telegram import Update
from telegram.ext import CommandHandler, ContextTypes
from service.flashscore_scraper import gerar_sugestoes_dia
from asyncio import to_thread

async def sugestao_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        await update.message.reply_text("🔍 Gerando sugestões com base nos jogos reais de hoje...")

        sugestoes = await to_thread(gerar_sugestoes_dia)

        if not sugestoes:
            await update.message.reply_text("⚠️ Nenhuma sugestão encontrada para hoje.")
            return

        for texto in sugestoes:
            await update.message.reply_text(texto, parse_mode="Markdown", disable_web_page_preview=False)

    except Exception as e:
        await update.message.reply_text(f"❌ Erro ao gerar sugestão: {e}")

def registrar_handlers_sugestao(app):
    app.add_handler(CommandHandler("sugestao", sugestao_handler))
