from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

from service.stats_service import listar_partidas_do_dia, obter_estatisticas_partida

# Comando /estatisticas
async def estatisticas_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    partidas = listar_partidas_do_dia()
    
    if not partidas:
        await update.message.reply_text("⚠️ Não foi possível encontrar partidas no Flashscore agora.")
        return

    keyboard = []
    for partida in partidas:
        texto_botao = f"{partida['hora']} - {partida['times']}"
        callback_data = f"estatisticas|{partida['url']}"
        keyboard.append([InlineKeyboardButton(texto_botao, callback_data=callback_data)])

    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "📊 *Escolha uma partida para ver as estatísticas reais:*",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )

# Callback ao clicar no botão
async def estatisticas_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data.startswith("estatisticas|"):
        _, url = query.data.split("|", 1)
        estatisticas = obter_estatisticas_partida(url)

        if not estatisticas:
            await query.edit_message_text("❌ Não foi possível obter as estatísticas desta partida.")
            return

        texto = (
            f"📈 *Estatísticas reais da partida:*\n\n"
            f"🏟️ *Times:* {estatisticas['times']}\n"
            f"⏰ *Horário:* {estatisticas['hora']}\n\n"
            f"🎯 *Finalizações:* {estatisticas['finalizacoes']}\n"
            f"🥅 *Chutes no Gol:* {estatisticas['chutes_no_gol']}\n"
            f"🚫 *Chutes para Fora:* {estatisticas['chutes_fora']}\n"
            f"🎯 *Posse de Bola:* {estatisticas['posse']}\n"
            f"🛡️ *Cartões Amarelos:* {estatisticas['amarelos']}\n"
            f"🔴 *Cartões Vermelhos:* {estatisticas['vermelhos']}\n"
            f"🚩 *Escanteios:* {estatisticas['escanteios']}\n"
        )

        await query.edit_message_text(texto, parse_mode="Markdown")

# Registro no bot
def registrar_handlers_estatisticas(app):
    app.add_handler(CommandHandler("estatisticas", estatisticas_handler))
    app.add_handler(CallbackQueryHandler(estatisticas_callback, pattern=r"^estatisticas\|"))
