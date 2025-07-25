from telegram import Update
from telegram.ext import CallbackContext

def start(update: Update, context: CallbackContext):
    message = (
        "👋 Olá! Sou seu bot de sugestões de apostas!\n\n"
        "📅 Use /hoje para ver os jogos de hoje\n"
        "📊 Use /estatisticas para ver estatísticas e análises\n"
        "💡 Use /sugestao para receber dicas de apostas"
    )
    update.message.reply_text(message)