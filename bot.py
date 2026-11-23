import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
import logging

load_dotenv()
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
logging.basicConfig(
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    level=logging.INFO,
)
# Библиотека httpx пишет в лог каждый запрос к Telegram, это шум, приглушаем
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger("fintra")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Salam! Mən Fintra 🛡\n"
        "Привет! Я Fintra 🛡\n"
        "Hi! I'm Fintra 🛡"
    )


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"Ты написала: {update.message.text}")

# Обработчик ошибок: логируем и вежливо отвечаем пользователю
async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    logger.error("Ошибка при обработке сообщения", exc_info=context.error)

    if isinstance(update, Update) and update.effective_message:
        await update.effective_message.reply_text(
            "⚠️ Xəta baş verdi / Произошла ошибка / Something went wrong. 🙏"
        )

def main():
    if not TOKEN:
        raise ValueError("TELEGRAM_BOT_TOKEN не найден в .env")

    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    app.add_error_handler(error_handler)

    logger.info("Fintra запущен... (остановить: Control + C)")
    app.run_polling()


if __name__ == "__main__":
    main()