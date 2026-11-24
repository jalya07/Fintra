import os
import logging
from dotenv import load_dotenv
from telegram import Update, BotCommand
from telegram.constants import ChatAction
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

from agent import run_agent
import database

# Загружаем ключи из .env
load_dotenv()
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

logging.basicConfig(
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    level=logging.INFO,
)
# Библиотека httpx пишет в лог каждый запрос к Telegram, это шум, приглушаем
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger("fintra")


# ---------- Команды ----------

# Ответ на команду /start
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


# ---------- Сообщения: текст, фото, голос ----------

# Общая логика: отправить агенту, показать шаги, вернуть картинки и текст
async def process_with_agent(update, context, text, media=None):
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id

    await context.bot.send_chat_action(chat_id=chat_id, action=ChatAction.TYPING)

    # Показываем пользователю каждый шаг агента
    async def show_step(tool_name):
        await context.bot.send_message(chat_id=chat_id, text=f"🔧 {tool_name}")
        await context.bot.send_chat_action(chat_id=chat_id, action=ChatAction.TYPING)

    reply, images = await run_agent(user_id, text, on_tool_call=show_step, media=media)

    # Сначала картинки (если инструменты их создали), потом текст
    for path in images:
        with open(path, "rb") as photo:
            await context.bot.send_photo(chat_id=chat_id, photo=photo)

    await update.message.reply_text(reply)


# Текстовое сообщение
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await process_with_agent(update, context, update.message.text)


# Фото (например, чек)
async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    photo = update.message.photo[-1]  # последнее = самое большое разрешение
    file = await photo.get_file()
    data = bytes(await file.download_as_bytearray())

    text = update.message.caption or "Here is a photo of my receipt."
    await process_with_agent(update, context, text, media=(data, "image/jpeg"))


# Голосовое сообщение
async def handle_voice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    file = await update.message.voice.get_file()
    data = bytes(await file.download_as_bytearray())

    text = "This is my voice message."
    await process_with_agent(update, context, text, media=(data, "audio/ogg"))


# ---------- Служебное ----------

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

    database.init_db()

    app = (
        Application.builder()
        .token(TOKEN)
        .post_init(set_commands)
        .concurrent_updates(True)
        .build()
    )

    # Команды
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))

    # Сообщения
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    app.add_handler(MessageHandler(filters.VOICE, handle_voice))

    app.add_error_handler(error_handler)

    logger.info("Fintra запущен... (остановить: Control + C)")
    app.run_polling()


if __name__ == "__main__":
    main()