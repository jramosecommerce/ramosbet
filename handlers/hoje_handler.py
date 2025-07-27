from telegram import Update
from telegram.ext import CommandHandler, ContextTypes
from service.flashscore_scraper import obter_jogos_do_dia
from asyncio import to_thread

async def hoje_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        await update.message.reply_text("📅 Buscando jogos reais de hoje...")

        # Correção: executa função síncrona via to_thread
        jogos = await to_thread(obter_jogos_do_dia)

        if not jogos:
            await update.message.reply_text("⚠️ Nenhum jogo encontrado para hoje.")
            return

        resposta = "*Jogos de hoje:*\n\n"
        for jogo in jogos:
            resposta += f"🏟️ {jogo['time_casa']} x {jogo['time_fora']}\n"
            resposta += f"[Estatísticas]({jogo['url_estatisticas']})\n\n"

        await update.message.reply_text(resposta, parse_mode="Markdown", disable_web_page_preview=False)

    except Exception as e:
        await update.message.reply_text(f"❌ Erro ao buscar jogos de hoje: {e}")

def registrar_handlers_hoje(app):
    app.add_handler(CommandHandler("hoje", hoje_handler))
