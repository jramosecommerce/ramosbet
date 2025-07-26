import os
from telegram.ext import ApplicationBuilder, CommandHandler
from handlers.start_handler import start
from handlers.hoje_handler import hoje_handler
from handlers.estatisticas_handler import registrar_handlers_estatisticas
from handlers.sugestao_handler import sugestao_handler
from service.scheduler import start_scheduler

TOKEN = os.getenv("BOT_TOKEN")

app = ApplicationBuilder().token(TOKEN).build()

# Registro dos comandos simples
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("hoje", hoje_handler))
app.add_handler(CommandHandler("sugestao", sugestao_handler))

# Registro do comando com callback (estatísticas por botão)
registrar_handlers_estatisticas(app)

# Agendamento da sugestão automática às 10h
chat_id_padrao = os.getenv("CHAT_ID_PADRAO")  # define o ID do grupo ou pessoa para envio automático
if chat_id_padrao:
    start_scheduler(app, int(chat_id_padrao))

print("✅ Bot iniciado com sucesso...")
app.run_polling()
