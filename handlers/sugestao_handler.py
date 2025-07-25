from telegram import Update
from telegram.ext import ContextTypes
from service.prediction_service import gerar_sugestoes

async def sugestao_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    sugestoes = gerar_sugestoes()
    await update.message.reply_text(sugestoes)