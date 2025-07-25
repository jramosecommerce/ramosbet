from telegram import Update
from telegram.ext import ContextTypes

async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🤖 Olá! Eu sou o seu bot de apostas. Use /hoje, /estatisticas ou /sugestao para começar.")