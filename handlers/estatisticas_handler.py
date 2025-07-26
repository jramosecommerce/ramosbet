from telegram import Update
from telegram.ext import CommandHandler, ContextTypes
from service.flashscore_scraper import obter_jogos_do_dia, obter_estatisticas_reais

async def estatisticas_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        jogos = await obter_jogos_do_dia()
        if not jogos:
            await update.message.reply_text("⚠️ Não foi possível encontrar partidas no Flashscore agora.")
            return

        jogo = jogos[0]  # Pega o primeiro jogo
        estatisticas = await obter_estatisticas_reais(jogo["url_estatisticas"])

        mensagem = (
            f"📊 *Estatísticas da Partida*\n\n"
            f"🏟️ {jogo['time_casa']} x {jogo['time_fora']}\n"
            f"🔗 [Ver no Flashscore]({jogo['url_estatisticas']})\n\n" +
            "\n".join(estatisticas)
        )

        await update.message.reply_text(mensagem)

    except Exception as e:
        await update.message.reply_text(f"❌ Erro ao buscar estatísticas: {e}")

def registrar_handlers_estatisticas(app):
    app.add_handler(CommandHandler("estatisticas", estatisticas_handler))
