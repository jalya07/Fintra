import os
from dotenv import load_dotenv
from telegram import Update, BotCommand
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

# Ответ на команду /help
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🛡 Fintra — AI finance agent\n\n"
        "🇦🇿 Xərclərini yaz, çekin şəklini göndər və ya səsli mesaj at — "
        "mən sayıram, planlayıram və qoruyuram.\n\n"
        "🇷🇺 Напиши трату, отправь фото чека или голосовое — "
        "я считаю, планирую и защищаю.\n\n"
        "🇬🇧 Type an expense, send a receipt photo or a voice message — "
        "I count, plan and protect.\n\n"
        "/start — Başla / Начать / Start\n"
        "/help — Kömək / Помощь / Help"
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

# Меню команд на трёх языках (выполняется один раз при запуске)
async def set_commands(app: Application):
    # По умолчанию (английский), для всех остальных языков
    await app.bot.set_my_commands([
        BotCommand("start", "Start Fintra"),
        BotCommand("help", "What can Fintra do?"),
    ])
    # Азербайджанский
    await app.bot.set_my_commands([
        BotCommand("start", "Fintra-nı başlat"),
        BotCommand("help", "Fintra nə edə bilər?"),
    ], language_code="az")
    # Русский
    await app.bot.set_my_commands([
        BotCommand("start", "Запустить Fintra"),
        BotCommand("help", "Что умеет Fintra?"),
    ], language_code="ru")

    logger.info("Меню команд установлено")

def main():
    if not TOKEN:
        raise ValueError("TELEGRAM_BOT_TOKEN не найден в .env")

    app = Application.builder().token(TOKEN).post_init(set_commands).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    app.add_error_handler(error_handler)

    logger.info("Fintra запущен... (остановить: Control + C)")
    app.run_polling()


if __name__ == "__main__":
    main()