from telegram import Update
from telegram.ext import ContextTypes

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    mensagem = (
        "👋 *Bem-vindo ao Bot de Apostas!*\n\n"
        "Use os comandos abaixo para começar:\n"
        "📅 /hoje – Ver jogos do dia\n"
        "📊 /estatisticas – Ver estatísticas reais por jogo\n"
        "💡 /sugestao – Receber uma sugestão de aposta"
    )
    await update.message.reply_text(mensagem, parse_mode="Markdown")
