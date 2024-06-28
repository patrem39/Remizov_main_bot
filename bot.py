from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

TOKEN = '7291732021:AAFhKuOkHHLrWp99cfRN6pnIQ4mwg22iEec'
WEBHOOK_URL = 'https://cloud.amvera.ru/projects/compute/telegrambot'

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Hello! This is a simple bot.')

def main() -> None:
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler('start', start))
    app.run_webhook(listen="0.0.0.0", port=8443, url_path=TOKEN, webhook_url=f"{WEBHOOK_URL}/{TOKEN}")

if __name__ == '__main__':
    main()
