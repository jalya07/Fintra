import re

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