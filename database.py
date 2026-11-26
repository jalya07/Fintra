import sqlite3
import hashlib
import secrets
from datetime import datetime, timedelta

DB_PATH = "fintra.db"


def get_connection():
    """Открывает соединение с базой. Строки можно читать по имени колонки."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def now_str():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def init_db():
    """Создаёт таблицы, если их ещё нет. Вызывается при запуске бота."""
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
        # План бюджета: одна строка на пользователя
        conn.execute("""
            CREATE TABLE IF NOT EXISTS budgets (
                user_id         INTEGER PRIMARY KEY,
                income          REAL    NOT NULL,
                payday          INTEGER NOT NULL,
                savings_percent REAL    NOT NULL,
                updated_at      TEXT    NOT NULL
            )
        """)
        # Обязательные платежи (аренда, кредит...)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS obligations (
                id      INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                name    TEXT    NOT NULL,
                amount  REAL    NOT NULL
            )
        """)
        # Лимиты на категорию или карту
        conn.execute("""
            CREATE TABLE IF NOT EXISTS limits (
                id         INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id    INTEGER NOT NULL,
                scope      TEXT    NOT NULL,   -- 'category' или 'card'
                target     TEXT    NOT NULL,   -- например 'cafe' или 'Birbank'
                amount     REAL    NOT NULL,
                created_at TEXT    NOT NULL,
                UNIQUE (user_id, scope, target)
            )
        """)
        # 🔐 Одноразовые коды для входа на сайт (хранится только хеш)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS web_tokens (
                token_hash TEXT PRIMARY KEY,
                user_id    INTEGER NOT NULL,
                expires_at TEXT    NOT NULL,
                used       INTEGER NOT NULL DEFAULT 0
            )
        """)
        # 🔐 Сессии сайта (хранится только хеш)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS web_sessions (
                session_hash TEXT PRIMARY KEY,
                user_id      INTEGER NOT NULL,
                expires_at   TEXT    NOT NULL
            )
        """)

# ---------- Траты ----------

def add_expense(user_id, amount, category, description=None,
                date=None, currency="AZN", card=None, source="text"):
    """Сохраняет трату и возвращает её id."""
    if date is None:
        date = datetime.now().strftime("%Y-%m-%d")

    with get_connection() as conn:
        cursor = conn.execute(
            """
            INSERT INTO expenses
                (user_id, amount, currency, category, description, card, date, source, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (user_id, amount, currency, category, description, card, date, source, now_str()),
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


def get_spent(user_id, start_date, end_date, category=None, card=None):
    """Сколько всего потрачено за период (можно по категории или по карте)."""
    query = "SELECT COALESCE(SUM(amount), 0) FROM expenses WHERE user_id = ? AND date BETWEEN ? AND ?"
    params = [user_id, start_date, end_date]

    if category:
        query += " AND category = ?"
        params.append(category)
    if card:
        query += " AND card = ?"
        params.append(card)

    with get_connection() as conn:
        return conn.execute(query, params).fetchone()[0]

def get_recent_expenses(user_id, limit=5):
    """Последние траты пользователя (самые новые сверху)."""
    with get_connection() as conn:
        rows = conn.execute(
            """
            SELECT amount, currency, category, description, card, date, source
            FROM expenses
            WHERE user_id = ?
            ORDER BY date DESC, id DESC
            LIMIT ?
            """,
            (user_id, limit),
        ).fetchall()
        return [dict(r) for r in rows]


def count_expenses(user_id, start_date, end_date):
    """Сколько трат за период."""
    with get_connection() as conn:
        return conn.execute(
            "SELECT COUNT(*) FROM expenses WHERE user_id = ? AND date BETWEEN ? AND ?",
            (user_id, start_date, end_date),
        ).fetchone()[0]

def get_expenses(user_id, start_date, end_date, category=None, source=None, limit=200):
    """Траты за период с фильтрами (самые новые сверху)."""
    query = """
        SELECT id, amount, currency, category, description, card, date, source
        FROM expenses
        WHERE user_id = ? AND date BETWEEN ? AND ?
    """
    params = [user_id, start_date, end_date]
    if category:
        query += " AND category = ?"
        params.append(category)
    if source:
        query += " AND source = ?"
        params.append(source)
    query += " ORDER BY date DESC, id DESC LIMIT ?"
    params.append(limit)

    with get_connection() as conn:
        return [dict(r) for r in conn.execute(query, params).fetchall()]


def delete_expense(user_id, expense_id):
    """🔐 Удаляет трату, только если она принадлежит этому пользователю."""
    with get_connection() as conn:
        cursor = conn.execute(
            "DELETE FROM expenses WHERE id = ? AND user_id = ?", (expense_id, user_id)
        )
        return cursor.rowcount > 0
# ---------- План бюджета ----------

def save_budget(user_id, income, payday, savings_percent, obligations):
    """Сохраняет план и обязательные платежи ОДНОЙ транзакцией.
    obligations = [{"name": "rent", "amount": 350}, ...]"""
    with get_connection() as conn:
        conn.execute(
            """
            INSERT INTO budgets (user_id, income, payday, savings_percent, updated_at)
            VALUES (?, ?, ?, ?, ?)
            ON CONFLICT(user_id) DO UPDATE SET
                income = excluded.income,
                payday = excluded.payday,
                savings_percent = excluded.savings_percent,
                updated_at = excluded.updated_at
            """,
            (user_id, income, payday, savings_percent, now_str()),
        )
        # Старые обязательные платежи заменяем новыми
        conn.execute("DELETE FROM obligations WHERE user_id = ?", (user_id,))
        for ob in obligations:
            conn.execute(
                "INSERT INTO obligations (user_id, name, amount) VALUES (?, ?, ?)",
                (user_id, ob["name"], ob["amount"]),
            )


def get_budget(user_id):
    """Возвращает план пользователя вместе с обязательными платежами, или None."""
    with get_connection() as conn:
        row = conn.execute("SELECT * FROM budgets WHERE user_id = ?", (user_id,)).fetchone()
        if row is None:
            return None
        obligations = conn.execute(
            "SELECT name, amount FROM obligations WHERE user_id = ?", (user_id,)
        ).fetchall()
        budget = dict(row)
        budget["obligations"] = [dict(o) for o in obligations]
        return budget


# ---------- Лимиты ----------

def set_limit(user_id, scope, target, amount):
    """Создаёт или обновляет лимит (на категорию или карту)."""
    with get_connection() as conn:
        conn.execute(
            """
            INSERT INTO limits (user_id, scope, target, amount, created_at)
            VALUES (?, ?, ?, ?, ?)
            ON CONFLICT(user_id, scope, target) DO UPDATE SET amount = excluded.amount
            """,
            (user_id, scope, target, amount, now_str()),
        )


def remove_limit(user_id, scope, target):
    """Удаляет лимит. Возвращает True, если лимит был."""
    with get_connection() as conn:
        cursor = conn.execute(
            "DELETE FROM limits WHERE user_id = ? AND scope = ? AND target = ?",
            (user_id, scope, target),
        )
        return cursor.rowcount > 0


def get_limits(user_id):
    """Все лимиты пользователя."""
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT scope, target, amount FROM limits WHERE user_id = ?", (user_id,)
        ).fetchall()
        return [dict(r) for r in rows]

# ---------- 🔐 Вход на сайт ----------

def _hash(token):
    """В базе храним только хеш: по нему нельзя восстановить сам код."""
    return hashlib.sha256(token.encode()).hexdigest()


def create_login_token(user_id, minutes=10):
    """Одноразовый код для входа. Возвращает сам код (он попадёт в ссылку)."""
    token = secrets.token_urlsafe(32)
    expires_at = (datetime.now() + timedelta(minutes=minutes)).strftime("%Y-%m-%d %H:%M:%S")
    with get_connection() as conn:
        conn.execute(
            "INSERT INTO web_tokens (token_hash, user_id, expires_at) VALUES (?, ?, ?)",
            (_hash(token), user_id, expires_at),
        )
    return token


def use_login_token(token):
    """Проверяет код и сразу «сжигает» его. Возвращает user_id или None."""
    token_hash = _hash(token)
    with get_connection() as conn:
        # Помечаем использованным, только если он не использован и не истёк
        cursor = conn.execute(
            "UPDATE web_tokens SET used = 1 WHERE token_hash = ? AND used = 0 AND expires_at > ?",
            (token_hash, now_str()),
        )
        if cursor.rowcount != 1:
            return None
        row = conn.execute(
            "SELECT user_id FROM web_tokens WHERE token_hash = ?", (token_hash,)
        ).fetchone()
        return row["user_id"]


def create_session(user_id, hours=24):
    """Новая сессия сайта. Возвращает код сессии (он попадёт в cookie)."""
    session_token = secrets.token_urlsafe(32)
    expires_at = (datetime.now() + timedelta(hours=hours)).strftime("%Y-%m-%d %H:%M:%S")
    with get_connection() as conn:
        conn.execute(
            "INSERT INTO web_sessions (session_hash, user_id, expires_at) VALUES (?, ?, ?)",
            (_hash(session_token), user_id, expires_at),
        )
    return session_token


def get_session_user(session_token):
    """Кто владелец сессии. None, если сессии нет или она истекла."""
    if not session_token:
        return None
    with get_connection() as conn:
        row = conn.execute(
            "SELECT user_id FROM web_sessions WHERE session_hash = ? AND expires_at > ?",
            (_hash(session_token), now_str()),
        ).fetchone()
        return row["user_id"] if row else None


def delete_session(session_token):
    """Выход: удаляем сессию."""
    if not session_token:
        return
    with get_connection() as conn:
        conn.execute("DELETE FROM web_sessions WHERE session_hash = ?", (_hash(session_token),))


def delete_user_sessions(user_id):
    """🔐 Выход на всех устройствах: удаляем все сессии пользователя."""
    with get_connection() as conn:
        conn.execute("DELETE FROM web_sessions WHERE user_id = ?", (user_id,))

# ---------- Данные пользователя (страница Security) ----------

def get_data_stats(user_id):
    """Сколько данных пользователя хранится: для страницы Security."""
    with get_connection() as conn:
        expenses = conn.execute(
            "SELECT COUNT(*) FROM expenses WHERE user_id = ?", (user_id,)
        ).fetchone()[0]
        limits = conn.execute(
            "SELECT COUNT(*) FROM limits WHERE user_id = ?", (user_id,)
        ).fetchone()[0]
        plan = conn.execute(
            "SELECT 1 FROM budgets WHERE user_id = ?", (user_id,)
        ).fetchone() is not None
        sessions = conn.execute(
            "SELECT COUNT(*) FROM web_sessions WHERE user_id = ? AND expires_at > ?",
            (user_id, now_str()),
        ).fetchone()[0]
    return {"expenses": expenses, "limits": limits, "plan": plan, "sessions": sessions}


def delete_user_data(user_id):
    """🔐 Удаляет ВСЕ данные пользователя одной транзакцией. Возвращает, сколько строк удалено."""
    counts = {}
    with get_connection() as conn:
        for table in ("expenses", "obligations", "limits", "budgets", "web_tokens", "web_sessions"):
            cursor = conn.execute(f"DELETE FROM {table} WHERE user_id = ?", (user_id,))
            counts[table] = cursor.rowcount
    return counts

# Быстрая проверка: запускается только при `python database.py`
if __name__ == "__main__":
    init_db()
    save_budget(1, 1000, 5, 10, [{"name": "rent", "amount": 350}, {"name": "loan", "amount": 120}])
    print("План:", get_budget(1))
    set_limit(1, "category", "cafe", 60)
    print("Лимиты:", get_limits(1))
    print("Потрачено на cafe:", get_spent(1, "2026-11-01", "2026-11-30", category="cafe"))