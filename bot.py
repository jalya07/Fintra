import os
import time
import secrets
import logging
from dotenv import load_dotenv
from telegram import Update, BotCommand, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.constants import ChatAction
from telegram.ext import (
    Application, CommandHandler, MessageHandler, CallbackQueryHandler,
    ContextTypes, filters,
)

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

# 🔐 Сколько секунд действует запрос на подтверждение
CONFIRM_TTL_SECONDS = 300


# ---------- Команды ----------

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Salam! Mən Fintra 🛡\n"
        "Привет! Я Fintra 🛡\n"
        "Hi! I'm Fintra 🛡"
    )


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


# ---------- 🔐 Подтверждение опасных действий ----------

def describe_confirmation(conf):
    """Текст запроса на трёх языках."""
    if conf["action"] == "remove_limit":
        return (
            "🔐 Limit silinsin? / Снять лимит? / Remove limit?\n"
            f"{conf['scope']}: {conf['target']} — {conf['amount']} AZN"
        )
    return "🔐 Təsdiq edin / Подтвердите / Please confirm"


async def ask_confirmation(update, context, conf):
    """Сохраняет запрос у себя и показывает кнопки. В кнопке — только случайный код."""
    token = secrets.token_hex(4)
    pending = context.user_data.setdefault("pending", {})
    pending[token] = {
        "data": conf,
        "user_id": update.effective_user.id,
        "created": time.time(),
    }

    keyboard = InlineKeyboardMarkup([[
        InlineKeyboardButton("✅ Bəli / Да / Yes", callback_data=f"confirm:{token}"),
        InlineKeyboardButton("❌ Xeyr / Нет / No", callback_data=f"cancel:{token}"),
    ]])
    await update.message.reply_text(describe_confirmation(conf), reply_markup=keyboard)


async def handle_confirmation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Нажатие кнопки. Действие выполняется только здесь — по нажатию человека."""
    query = update.callback_query
    await query.answer()

    action, token = query.data.split(":", 1)
    item = context.user_data.get("pending", {}).pop(token, None)

    # Запроса нет или кнопку нажал не тот пользователь
    if item is None or item["user_id"] != query.from_user.id:
        await query.edit_message_text("⚠️ Sorğu tapılmadı / Запрос не найден / Request not found")
        return

    # Запрос устарел
    if time.time() - item["created"] > CONFIRM_TTL_SECONDS:
        await query.edit_message_text("⌛ Vaxt bitdi / Время истекло / Request expired")
        return

    if action == "cancel":
        await query.edit_message_text("❌ Ləğv edildi / Отменено / Cancelled")
        return

    conf = item["data"]
    if conf["action"] == "remove_limit":
        removed = database.remove_limit(item["user_id"], conf["scope"], conf["target"])
        logger.info("Пользователь %s подтвердил снятие лимита %s:%s",
                    item["user_id"], conf["scope"], conf["target"])
        if removed:
            await query.edit_message_text("✅ Limit silindi / Лимит снят / Limit removed")
        else:
            await query.edit_message_text("⚠️ Limit tapılmadı / Лимит не найден / Limit not found")


# ---------- Сообщения: текст, фото, голос ----------

async def process_with_agent(update, context, text, media=None):
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id

    await context.bot.send_chat_action(chat_id=chat_id, action=ChatAction.TYPING)

    # Показываем пользователю каждый шаг агента
    async def show_step(tool_name):
        await context.bot.send_message(chat_id=chat_id, text=f"🔧 {tool_name}")
        await context.bot.send_chat_action(chat_id=chat_id, action=ChatAction.TYPING)

    reply, images, confirmations = await run_agent(
        user_id, text, on_tool_call=show_step, media=media
    )

    # Сначала картинки (если инструменты их создали)
    for path in images:
        with open(path, "rb") as photo:
            await context.bot.send_photo(chat_id=chat_id, photo=photo)

    # Потом ответ агента
    await update.message.reply_text(reply)

    # 🔐 И кнопки подтверждения, если агент попросил опасное действие
    for conf in confirmations:
        await ask_confirmation(update, context, conf)


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await process_with_agent(update, context, update.message.text)


async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    photo = update.message.photo[-1]  # последнее = самое большое разрешение
    file = await photo.get_file()
    data = bytes(await file.download_as_bytearray())

    text = update.message.caption or "Here is a photo of my receipt."
    await process_with_agent(update, context, text, media=(data, "image/jpeg"))


async def handle_voice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    file = await update.message.voice.get_file()
    data = bytes(await file.download_as_bytearray())

    text = "This is my voice message."
    await process_with_agent(update, context, text, media=(data, "audio/ogg"))


# ---------- Служебное ----------

async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    logger.error("Ошибка при обработке сообщения", exc_info=context.error)

    if isinstance(update, Update) and update.effective_message:
        await update.effective_message.reply_text(
            "⚠️ Xəta baş verdi / Произошла ошибка / Something went wrong. 🙏"
        )


async def set_commands(app: Application):
    await app.bot.set_my_commands([
        BotCommand("start", "Start Fintra"),
        BotCommand("help", "What can Fintra do?"),
    ])
    await app.bot.set_my_commands([
        BotCommand("start", "Fintra-nı başlat"),
        BotCommand("help", "Fintra nə edə bilər?"),
    ], language_code="az")
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

    # 🔐 Кнопки подтверждения
    app.add_handler(CallbackQueryHandler(handle_confirmation, pattern=r"^(confirm|cancel):"))

    # Сообщения
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    app.add_handler(MessageHandler(filters.VOICE, handle_voice))

    app.add_error_handler(error_handler)

    logger.info("Fintra запущен... (остановить: Control + C)")
    app.run_polling()


if __name__ == "__main__":
    main()