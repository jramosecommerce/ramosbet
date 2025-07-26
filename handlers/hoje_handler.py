from telegram import Update
from telegram.ext import CommandHandler, ContextTypes
from service.flashscore_scraper import obter_jogos_do_dia

async def hoje_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        jogos = await obter_jogos_do_dia()

        if not jogos:
            await update.message.reply_text("⚠️ Não há jogos marcados para hoje.")
            return

        mensagem = "📅 *Jogos de Hoje:*\n\n"
        for jogo in jogos[:10]:
            mensagem += f"⚽ {jogo['time_casa']} x {jogo['time_fora']}\n🔗 {jogo['url_estatisticas']}\n\n"

        await update.message.reply_text(mensagem)

    except Exception as e:
        await update.message.reply_text(f"❌ Erro ao buscar jogos de hoje: {e}")

def registrar_handlers_hoje(app):
    app.add_handler(CommandHandler("hoje", hoje_handler))
