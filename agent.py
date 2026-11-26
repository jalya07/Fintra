import os
import logging
from dotenv import load_dotenv
from google import genai
from google.genai import types, errors

from tools import TOOL_DECLARATIONS, execute_tool
from prompts import build_system_prompt

load_dotenv()
logger = logging.getLogger("fintra.agent")

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Список моделей по приоритету: если первая недоступна, пробуем следующую
GEMINI_MODELS = os.getenv(
    "GEMINI_MODELS", "gemini-3.7-flash,gemini-3.6-flash,gemini-3.5-flash"
).split(",")

client = genai.Client(
    api_key=GEMINI_API_KEY,
    http_options=types.HttpOptions(timeout=15_000),  # 15 секунд
)

# Коды ошибок, при которых есть смысл попробовать другую модель
RETRYABLE_CODES = {429, 500, 503}

# Защита от бесконечного цикла
MAX_STEPS = 5


async def generate_with_fallback(contents, config):
    """Запрос к Gemini с перебором моделей."""
    last_error = None

    for model in GEMINI_MODELS:
        model = model.strip()
        try:
            response = await client.aio.models.generate_content(
                model=model, contents=contents, config=config,
            )
            logger.info("Ответила модель: %s", model)
            return response

        except errors.APIError as e:
            if e.code in RETRYABLE_CODES:
                logger.warning("Модель %s недоступна (%s), пробую следующую", model, e.code)
                last_error = e
                continue
            raise  # другие ошибки (например, неверный ключ) не скрываем

        except Exception as e:
            logger.warning("Модель %s не ответила (%s), пробую следующую", model, type(e).__name__)
            last_error = e
            continue

    raise last_error


async def run_agent(user_id, user_text, on_tool_call=None, media=None):
    """Цикл агента. media = (байты файла, тип), например фото или голос.
    Возвращает (текст ответа, картинки, запросы на подтверждение)."""
    config = types.GenerateContentConfig(
        system_instruction=build_system_prompt(),
        tools=[types.Tool(function_declarations=TOOL_DECLARATIONS)],
        # Цикл ведём сами, чтобы подставлять user_id и показывать шаги
        automatic_function_calling=types.AutomaticFunctionCallingConfig(disable=True),
    )

    # Сообщение пользователя: текст + (если есть) фото или аудио
    parts = [types.Part.from_text(text=user_text)]
    if media:
        data, mime_type = media
        parts.append(types.Part.from_bytes(data=data, mime_type=mime_type))

    contents = [types.Content(role="user", parts=parts)]
    images = []         # картинки, которые создали инструменты
    confirmations = []  # 🔐 действия, которые должен подтвердить человек
    banners = []        # 🔐 плашки риска от кода (модель не может их изменить)

    for step in range(1, MAX_STEPS + 1):
        response = await generate_with_fallback(contents, config)

        # Модель не просит инструментов → это финальный ответ
        if not response.function_calls:
            reply = response.text
            if banners:
                reply = "\n".join(banners) + "\n\n" + reply
            return reply, images, confirmations

        # Сохраняем «решение» модели в историю
        contents.append(response.candidates[0].content)

        # Выполняем каждый инструмент, который она попросила
        result_parts = []
        for call in response.function_calls:
            args = dict(call.args) if call.args else {}
            logger.info("Шаг %d: вызываю %s(%s)", step, call.name, args)

            if on_tool_call:
                await on_tool_call(call.name)

            result = execute_tool(call.name, args, user_id)

            if isinstance(result, dict):
                if result.get("chart_path"):
                    images.append(result["chart_path"])
                if result.get("confirmation"):
                    confirmations.append(result["confirmation"])
                if result.get("risk_banner"):
                    banners.append(result["risk_banner"])

            result_parts.append(
                types.Part.from_function_response(name=call.name, response={"result": result})
            )

        # Возвращаем результаты модели, и цикл продолжается
        contents.append(types.Content(role="user", parts=result_parts))

    return "⚠️ Çox addım oldu / Слишком много шагов / Too many steps. 🙏", images, confirmations