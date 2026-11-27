import os
import json
import logging
from dotenv import load_dotenv
from google import genai
from google.genai import types, errors
from openai import AsyncOpenAI

import security
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


# ---------- 🛟 Резервные провайдеры (OpenAI-совместимый формат) ----------

def _split(value):
    """'a,b,,c' -> ['a', 'b', 'c']"""
    return [v.strip() for v in (value or "").split(",") if v.strip()]


def build_fallback_providers():
    """Цепочка резерва: сначала OpenRouter (облако), потом Ollama (на этом компьютере).
    Провайдер без настроек в .env просто пропускается."""
    providers = []

    openrouter_key = os.getenv("OPENROUTER_API_KEY")
    openrouter_models = _split(os.getenv("OPENROUTER_MODELS"))
    if openrouter_key and openrouter_models:
        providers.append({
            "name": "OpenRouter",
            "client": AsyncOpenAI(base_url="https://openrouter.ai/api/v1",
                                  api_key=openrouter_key, timeout=25),
            "models": openrouter_models,
        })

    ollama_models = _split(os.getenv("OLLAMA_MODELS"))
    if ollama_models:
        providers.append({
            "name": "Ollama",
            "client": AsyncOpenAI(base_url=os.getenv("OLLAMA_URL", "http://localhost:11434/v1"),
                                  api_key="ollama", timeout=60),  # 🔐 данные не покидают компьютер
            "models": ollama_models,
            # Выключаем «режим размышлений»: иначе локальная модель думает минутами
            "extra": {"reasoning_effort": "none"},
        })
    return providers


FALLBACK_PROVIDERS = build_fallback_providers()


def to_openai_tools(declarations):
    """Наши описания инструментов (формат Gemini) -> формат OpenAI."""
    result = []
    for d in declarations:
        get = d.get if isinstance(d, dict) else (lambda key, obj=d: getattr(obj, key, None))
        params = (get("parameters_json_schema") or get("parameters")
                  or {"type": "object", "properties": {}})
        result.append({
            "type": "function",
            "function": {"name": get("name"), "description": get("description") or "",
                         "parameters": params},
        })
    return result


OPENAI_TOOLS = to_openai_tools(TOOL_DECLARATIONS)

MEDIA_UNAVAILABLE = (
    "⚠️ Foto və səs hazırda müvəqqəti işləmir, zəhmət olmasa mətnlə yazın.\n"
    "⚠️ Фото и голос сейчас временно недоступны, пожалуйста, напишите текстом.\n"
    "⚠️ Photos and voice are temporarily unavailable, please type your message."
)
ALL_DOWN = (
    "⚠️ Xidmət müvəqqəti əlçatan deyil, bir az sonra yenidən cəhd edin.\n"
    "⚠️ Сервис временно недоступен, попробуйте чуть позже.\n"
    "⚠️ The service is temporarily unavailable, please try again later."
)
TOO_MANY_STEPS = "⚠️ Çox addım oldu / Слишком много шагов / Too many steps. 🙏"


# ---------- Общие помощники ----------

def collect(result, images, confirmations, banners):
    """Забираем из результата инструмента то, что обрабатывает код, а не модель."""
    if isinstance(result, dict):
        if result.get("chart_path"):
            images.append(result["chart_path"])
        if result.get("confirmation"):
            confirmations.append(result["confirmation"])
        if result.get("risk_banner") and result["risk_banner"] not in banners:
            banners.append(result["risk_banner"])


def with_banners(reply, banners):
    """🔐 Плашки риска от кода ставим перед ответом: модель не может их убрать."""
    reply = reply or ""
    if banners:
        reply = "\n".join(dict.fromkeys(banners)) + "\n\n" + reply   # без повторов
    return reply


# ---------- Gemini ----------

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


async def run_gemini(user_id, user_text, on_tool_call, media, executed,
                     images, confirmations, banners):
    """Цикл агента на Gemini. Каждый выполненный шаг записываем в executed,
    чтобы резервная модель не повторила его, если Gemini упадёт посередине."""
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

    for step in range(1, MAX_STEPS + 1):
        response = await generate_with_fallback(contents, config)

        # Модель не просит инструментов → это финальный ответ
        if not response.function_calls:
            return with_banners(response.text, banners)

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
            executed.append((call.name, args, result))
            collect(result, images, confirmations, banners)

            result_parts.append(
                types.Part.from_function_response(name=call.name, response={"result": result})
            )

        # Возвращаем результаты модели, и цикл продолжается
        contents.append(types.Content(role="user", parts=result_parts))

    return TOO_MANY_STEPS


# ---------- 🛟 Резерв: OpenRouter / Ollama ----------

async def chat_with_fallback(messages):
    """Перебираем резервных провайдеров и их модели по очереди."""
    last_error = None
    for provider in FALLBACK_PROVIDERS:
        for model in provider["models"]:
            try:
                response = await provider["client"].chat.completions.create(
                    model=model, messages=messages, tools=OPENAI_TOOLS,
                    **provider.get("extra", {}),
                )
                logger.info("🛟 Ответил резерв: %s / %s", provider["name"], model)
                return response.choices[0].message
            except Exception as e:
                logger.warning("🛟 %s / %s не ответил (%s), пробую дальше",
                               provider["name"], model, type(e).__name__)
                last_error = e
    raise last_error or RuntimeError("no fallback providers configured")


async def run_fallback(user_id, user_text, on_tool_call, executed,
                       images, confirmations, banners):
    """Тот же цикл агента, но в формате OpenAI (OpenRouter и Ollama его понимают)."""
    messages = [
        {"role": "system", "content": build_system_prompt()},
        {"role": "user", "content": user_text},
    ]

    # Шаги, которые Gemini уже успел выполнить, передаём как историю → они не повторятся
    for i, (name, args, result) in enumerate(executed):
        call_id = f"done_{i}"
        messages.append({"role": "assistant", "content": None, "tool_calls": [{
            "id": call_id, "type": "function",
            "function": {"name": name, "arguments": json.dumps(args, ensure_ascii=False)},
        }]})
        messages.append({"role": "tool", "tool_call_id": call_id,
                         "content": json.dumps({"result": result}, ensure_ascii=False, default=str)})

    for step in range(1, MAX_STEPS + 1):
        message = await chat_with_fallback(messages)

        if not message.tool_calls:
            return with_banners(message.content, banners)

        messages.append({"role": "assistant", "content": message.content or None,
                         "tool_calls": [tc.model_dump() for tc in message.tool_calls]})

        for tc in message.tool_calls:
            try:
                args = json.loads(tc.function.arguments or "{}")
            except json.JSONDecodeError:
                args = {}
            logger.info("🛟 Шаг %d: вызываю %s(%s)", step, tc.function.name, args)

            if on_tool_call:
                await on_tool_call(tc.function.name)

            # 🔐 user_id подставляет код, а не модель: чужие данные недоступны
            result = execute_tool(tc.function.name, args, user_id)
            collect(result, images, confirmations, banners)
            messages.append({"role": "tool", "tool_call_id": tc.id,
                             "content": json.dumps({"result": result}, ensure_ascii=False, default=str)})

    return TOO_MANY_STEPS


# ---------- Главная функция ----------

async def run_agent(user_id, user_text, on_tool_call=None, media=None):
    """Цикл агента. media = (байты файла, тип), например фото или голос.
    Возвращает (текст ответа, картинки, запросы на подтверждение)."""
    images = []         # картинки, которые создали инструменты
    confirmations = []  # 🔐 действия, которые должен подтвердить человек
    banners = []        # 🔐 плашки риска от кода (модель не может их изменить)
    executed = []       # уже выполненные шаги: (имя, аргументы, результат)

    # 🔐 Правила мошенничества проверяют КАЖДОЕ сообщение ещё до модели.
    # Даже если модель забудет вызвать check_scam (так делала локальная модель в тестах),
    # пользователь всё равно увидит предупреждение от кода.
    rules = security.analyze_scam(user_text or "")
    if rules.get("rule_risk") in ("high", "medium"):
        banner = security.RISK_BANNERS.get(rules["rule_risk"])
        if banner:
            banners.append(banner)

    try:
        reply = await run_gemini(user_id, user_text, on_tool_call, media, executed,
                                 images, confirmations, banners)
        return reply, images, confirmations
    except Exception as e:
        logger.error("Gemini недоступен (%s), включаю резерв", type(e).__name__)

    # Фото и голос резерв не понимает: просим написать текстом
    if media and not executed:
        return MEDIA_UNAVAILABLE, images, confirmations

    try:
        reply = await run_fallback(user_id, user_text, on_tool_call, executed,
                                   images, confirmations, banners)
    except Exception as e:
        logger.error("Резерв тоже недоступен (%s)", type(e).__name__)
        reply = with_banners(ALL_DOWN, banners)
    return reply, images, confirmations
