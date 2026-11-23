import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters


load_dotenv()
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Salam! Mən Fintra 🛡\n"
        "Привет! Я Fintra 🛡\n"
        "Hi! I'm Fintra 🛡"
    )


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"Ты написала: {update.message.text}")


def main():
    if not TOKEN:
        raise ValueError("TELEGRAM_BOT_TOKEN не найден в .env")

    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    print("Fintra запущен... (остановить: Control + C)")
    app.run_polling()


if __name__ == "__main__":
    main()