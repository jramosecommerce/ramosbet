from telegram import Update
from telegram.ext import CommandHandler, ContextTypes
from service.stats_service import obter_estatisticas_reais

async def estatisticas_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        if not context.args:
            await update.message.reply_text("ℹ️ Use assim: `/estatisticas ID_DA_PARTIDA`", parse_mode="Markdown")
            return

        id_partida = context.args[0]
        texto = obter_estatisticas_reais(id_partida)

        await update.message.reply_text(texto, parse_mode="Markdown")

    except Exception as e:
        await update.message.reply_text(f"❌ Erro ao buscar estatísticas: {e}")

def registrar_handlers_estatisticas(app):
    app.add_handler(CommandHandler("estatisticas", estatisticas_handler))
