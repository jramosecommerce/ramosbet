from telegram import Update
from telegram.ext import ContextTypes
from service.stats_service import get_past_match_stats

async def estatisticas_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    stats = get_past_match_stats()
    if not stats:
        await update.message.reply_text("Sem estatísticas disponíveis no momento.")
        return
    response = "📊 *Estatísticas Recentes:*\n\n"
    for s in stats:
        response += f"{s['match']}: Gols: {s['goals']}, Escanteios: {s['corners']}, Cartões: {s['cards']}\n"
    await update.message.reply_text(response, parse_mode="Markdown")