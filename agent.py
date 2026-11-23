import os
import logging
from dotenv import load_dotenv
from google import genai
from google.genai import types
from google.genai import errors

load_dotenv()
logger = logging.getLogger("fintra.agent")

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
# Список моделей по приоритету: если первая недоступна, пробуем следующую
GEMINI_MODELS = os.getenv(
    "GEMINI_MODELS", "gemini-3.7-flash,gemini-3.6-flash,gemini-3.5-flash"
).split(",")

client = genai.Client(
    api_key=GEMINI_API_KEY,
    http_options=types.HttpOptions(timeout=15_000),  # 15 секунд, в миллисекундах
)

# Временный системный промпт. Полный напишем позже через мета-промпт
SYSTEM_PROMPT = (
    "You are Fintra, a friendly AI finance agent in Telegram. "
    "Always reply in the same language the user writes in "
    "(Azerbaijani, Russian or English). "
    "Keep answers short and clear."
)


# Коды ошибок, при которых есть смысл попробовать другую модель
RETRYABLE_CODES = {429, 500, 503}


async def ask_agent(user_text: str) -> str:
    """Отправляет текст в Gemini. Если модель недоступна, пробует следующую."""
    last_error = None

    for model in GEMINI_MODELS:
        model = model.strip()
        try:
            response = await client.aio.models.generate_content(
                model=model,
                contents=user_text,
                config=types.GenerateContentConfig(
                    system_instruction=SYSTEM_PROMPT,
                ),
            )
            logger.info("Ответила модель: %s", model)
            return response.text

        except errors.APIError as e:
            if e.code in RETRYABLE_CODES:
                logger.warning("Модель %s недоступна (%s), пробую следующую", model, e.code)
                last_error = e
                continue
            raise # другие ошибки (например, неверный ключ) не скрываем
        except Exception as e:
            # Таймаут или сетевая ошибка: тоже пробуем следующую модель
            logger.warning("Модель %s не ответила (%s), пробую следующую", model, type(e).__name__)
            last_error = e
            continue

    # Все модели недоступны
    raise last_error