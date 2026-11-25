import re
from urllib.parse import urlparse

# ==================== Номера карт ====================

# 13–19 цифр подряд, можно с пробелами или дефисами (как пишут номер карты)
CARD_PATTERN = re.compile(r"(?:\d[ -]?){13,19}")


def luhn_valid(number: str) -> bool:
    """Алгоритм Луна: так проверяют, похожа ли строка цифр на настоящий номер карты."""
    digits = [int(d) for d in number]
    checksum = 0
    parity = len(digits) % 2
    for i, d in enumerate(digits):
        if i % 2 == parity:
            d *= 2
            if d > 9:
                d -= 9
        checksum += d
    return checksum % 10 == 0


def find_card_numbers(text: str) -> list:
    """Находит в тексте номера банковских карт."""
    if not text:
        return []
    found = []
    for match in CARD_PATTERN.finditer(text):
        digits = re.sub(r"\D", "", match.group())
        if 13 <= len(digits) <= 19 and luhn_valid(digits):
            found.append(digits)
    return found


def looks_like_card_number(text: str) -> bool:
    return bool(find_card_numbers(text))


# ==================== Мошенничество ====================

# Просьба сообщить секретные данные. Банк НИКОГДА об этом не просит
SECRET_WORDS = [
    "cvv", "cvc", "pin", "otp", "sms kod", "smskod", "kodu", "şifrə", "sifre",
    "код из sms", "смс код", "смс-код", "код подтверждения", "пароль",
    "password", "verification code", "one-time code",
]

# Давление срочностью и угрозы
URGENCY_WORDS = [
    "təcili", "dərhal", "24 saat", "bloklan", "dondurul",
    "срочно", "немедленно", "24 час", "заблокир",
    "urgent", "immediately", "within 24", "blocked", "suspended",
]

# Обещание выигрыша
PRIZE_WORDS = [
    "uddunuz", "qazandınız", "hədiyyə", "bonus",
    "выиграли", "приз", "подарок",
    "you won", "winner", "prize", "gift",
]

# Сокращатели ссылок: прячут настоящий адрес
SHORTENERS = ["bit.ly", "tinyurl.com", "cutt.ly", "t.ly", "is.gd", "goo.gl", "rb.gy", "shorturl.at"]

# ⚠️ Официальные домены. ПРОВЕРЬ каждый на официальном сайте банка перед демо!
OFFICIAL_DOMAINS = [
    "kapitalbank.az", "birbank.az", "abb-bank.az", "pashabank.az",
    "bankrespublika.az", "unibank.az", "xalqbank.az", "accessbank.az",
    "leobank.az", "yelo.az",
]

# Названия, которые мошенники вставляют в поддельные адреса
BRAND_WORDS = ["kapital", "birbank", "abb", "pasha", "respublika",
               "unibank", "xalq", "accessbank", "leobank", "yelo"]

URL_PATTERN = re.compile(
    r"(?:https?://|www\.)\S+|\b[\w-]+(?:\.[\w-]+)*\.(?:az|com|net|org|info|xyz|top|site|online|ru)\b\S*",
    re.IGNORECASE,
)


def _contains_any(text, words):
    return [w for w in words if w in text]


def _is_official(host):
    """Домен официальный, если совпадает с официальным или это его поддомен."""
    return any(host == d or host.endswith("." + d) for d in OFFICIAL_DOMAINS)


def check_links(text):
    """Проверяет все ссылки в тексте. Возвращает список найденных проблем."""
    flags = []
    for url in URL_PATTERN.findall(text):
        full = url if url.lower().startswith("http") else "http://" + url
        host = (urlparse(full).hostname or "").lower()
        if not host:
            continue

        if host in SHORTENERS:
            flags.append(f"shortened link hides the real address: {host}")
        if re.fullmatch(r"[\d.]+", host):
            flags.append(f"link uses an IP address instead of a domain: {host}")
        if full.lower().startswith("http://") and url.lower().startswith("http://"):
            flags.append(f"link is not secure (no HTTPS): {host}")
        if any(b in host for b in BRAND_WORDS) and not _is_official(host):
            flags.append(f"looks like a bank site but is NOT an official domain: {host}")
    return flags


def analyze_scam(text: str) -> dict:
    """Правила в коде. Возвращает уровень риска и найденные признаки."""
    low = (text or "").lower()
    flags = []

    secrets_found = _contains_any(low, SECRET_WORDS)
    urgency_found = _contains_any(low, URGENCY_WORDS)
    prize_found = _contains_any(low, PRIZE_WORDS)
    link_flags = check_links(low)

    if secrets_found:
        flags.append("asks for secret data (CVV, PIN, SMS code or password) — banks never do this")
    if urgency_found:
        flags.append("pressure with urgency or threats (blocked card, 24 hours)")
    if prize_found:
        flags.append("promises a prize or gift")
    flags.extend(link_flags)

    # Уровень риска по правилам
    if secrets_found or any("NOT an official" in f or "IP address" in f for f in link_flags):
        risk = "high"
    elif urgency_found and link_flags:
        risk = "high"
    elif urgency_found or prize_found or link_flags:
        risk = "medium"
    else:
        risk = "none_found"

    return {"rule_risk": risk, "red_flags": flags}


# Плашка, которую добавляет КОД (модель не может её изменить)
RISK_BANNERS = {
    "high": "🚨 Yüksək risk / Высокий риск / High risk",
    "medium": "⚠️ Orta risk / Средний риск / Medium risk",
}