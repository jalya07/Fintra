import sqlite3
from datetime import datetime

DB_PATH = "fintra.db"


def get_connection():
    """Открывает соединение с базой. Строки можно читать по имени колонки."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Создаёт таблицу, если её ещё нет. Вызывается при запуске бота."""
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS expenses (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id     INTEGER NOT NULL,
                amount      REAL    NOT NULL,
                currency    TEXT    NOT NULL DEFAULT 'AZN',
                category    TEXT    NOT NULL,
                description TEXT,
                card        TEXT,
                date        TEXT    NOT NULL,
                source      TEXT    NOT NULL DEFAULT 'text',
                created_at  TEXT    NOT NULL
            )
        """)


def add_expense(user_id, amount, category, description=None,
                date=None, currency="AZN", card=None, source="text"):
    """Сохраняет трату и возвращает её id."""
    if date is None:
        date = datetime.now().strftime("%Y-%m-%d")
    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with get_connection() as conn:
        cursor = conn.execute(
            """
            INSERT INTO expenses
                (user_id, amount, currency, category, description, card, date, source, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (user_id, amount, currency, category, description, card, date, source, created_at),
        )
        return cursor.lastrowid


def get_summary(user_id, start_date, end_date, category=None):
    """Итоги по категориям за период: сумма и количество покупок."""
    query = """
        SELECT category, SUM(amount) AS total, COUNT(*) AS count
        FROM expenses
        WHERE user_id = ? AND date BETWEEN ? AND ?
    """
    params = [user_id, start_date, end_date]

    if category:
        query += " AND category = ?"
        params.append(category)

    query += " GROUP BY category ORDER BY total DESC"

    with get_connection() as conn:
        rows = conn.execute(query, params).fetchall()
        return [dict(row) for row in rows]


# Быстрая проверка: запускается только при `python database.py`
if __name__ == "__main__":
    init_db()
    new_id = add_expense(user_id=1, amount=3.5, category="cafe", description="test coffee")
    print("Добавлена запись с id:", new_id)
    print(get_summary(user_id=1, start_date="2026-01-01", end_date="2026-12-31"))