from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import CommandHandler, CallbackQueryHandler, ContextTypes
from service.flashscore_scraper import obter_jogos_do_dia, obter_estatisticas_reais
from asyncio import to_thread

# Armazena os jogos do dia em cache simples por usuário
jogos_cache = {}

async def estatisticas_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        await update.message.reply_text("📊 Buscando jogos disponíveis para mostrar estatísticas reais...")

        # Executa função síncrona em thread
        jogos = await to_thread(obter_jogos_do_dia)

        if not jogos:
            await update.message.reply_text("⚠️ Nenhum jogo encontrado.")
            return

        # Salva os jogos no cache do usuário
        jogos_cache[update.effective_chat.id] = jogos

        botoes = [
            [InlineKeyboardButton(jogo, callback_data=str(i))] for i, jogo in enumerate(jogos)
        ]

        await update.message.reply_text(
            "Selecione uma partida para ver as estatísticas reais:",
            reply_markup=InlineKeyboardMarkup(botoes)
        )

    except Exception as e:
        await update.message.reply_text(f"❌ Erro ao carregar estatísticas: {e}")

async def estatisticas_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        query = update.callback_query
        await query.answer()

        jogos = jogos_cache.get(update.effective_chat.id)
        if not jogos:
            await query.edit_message_text("⚠️ Nenhuma partida encontrada no cache.")
            return

        indice = int(query.data)
        jogo = jogos[indice]

        # Chama função de scraping de estatísticas com a string do jogo
        estatisticas = await to_thread(obter_estatisticas_reais, jogo)

        texto = (
            f"📊 *Estatísticas Reais*\n"
            f"🏟️ {jogo}\n\n" +
            "\n".join(estatisticas)
        )

        await query.edit_message_text(texto, parse_mode="Markdown")

    except Exception as e:
        await update.effective_message.reply_text(f"❌ Erro: {e}")

def registrar_handlers_estatisticas(app):
    app.add_handler(CommandHandler("estatisticas", estatisticas_handler))
    app.add_handler(CallbackQueryHandler(estatisticas_callback))
