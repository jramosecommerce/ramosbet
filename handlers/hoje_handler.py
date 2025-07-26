from telegram import Update
from telegram.ext import ContextTypes
from service.flashscore_scraper import obter_jogos_do_dia

async def hoje_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    jogos = await obter_jogos_do_dia()  # ← CORRIGIDO: adiciona await

    if not jogos:
        await update.message.reply_text("⚠️ Não há jogos marcados para hoje.")
        return

    mensagem = "📅 *Jogos de Hoje:*\n\n"
    for jogo in jogos:
        mensagem += f"⏰ {jogo['horario']} - {jogo['time_casa']} x {jogo['time_fora']}\n"
    
    await update.message.reply_text(mensagem, parse_mode="Markdown")
