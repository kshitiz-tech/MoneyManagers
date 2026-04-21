from __future__ import annotations

import hashlib
import os
import sqlite3
from contextlib import contextmanager
from datetime import date, datetime
from pathlib import Path
from typing import Any


APP_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = APP_DIR / "data"
DB_PATH = DATA_DIR / "money_manager.db"
OUTBOX_PATH = DATA_DIR / "outbox.log"

CATEGORIES = [
    "Housing",
    "Food",
    "Transportation",
    "Entertainment",
    "Savings",
    "Utilities",
    "Health",
    "Education",
    "Misc",
]

CURRENCIES = ["USD", "EUR", "GBP", "NPR", "JPY"]
THEMES = ["Light", "Dark"]


def _dict_factory(cursor: sqlite3.Cursor, row: tuple[Any, ...]) -> dict[str, Any]:
    return {column[0]: row[index] for index, column in enumerate(cursor.description)}


class Database:
    def __init__(self, db_path: Path = DB_PATH) -> None:
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        self.db_path = db_path
        self.initialize()

    @contextmanager
    def connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self.db_path)
        connection.row_factory = _dict_factory
        try:
            yield connection
            connection.commit()
        finally:
            connection.close()

    def initialize(self) -> None:
        with self.connect() as connection:
            connection.executescript(
                """
                PRAGMA foreign_keys = ON;

                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    full_name TEXT NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    password_hash TEXT NOT NULL,
                    password_salt TEXT NOT NULL,
                    created_at TEXT NOT NULL
                );

                CREATE TABLE IF NOT EXISTS settings (
                    user_id INTEGER PRIMARY KEY,
                    notifications_enabled INTEGER NOT NULL DEFAULT 1,
                    email_alerts_enabled INTEGER NOT NULL DEFAULT 0,
                    email_address TEXT,
                    currency TEXT NOT NULL DEFAULT 'USD',
                    theme TEXT NOT NULL DEFAULT 'Light',
                    FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
                );

                CREATE TABLE IF NOT EXISTS transactions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    transaction_type TEXT NOT NULL CHECK(transaction_type IN ('income', 'expense')),
                    category TEXT NOT NULL,
                    amount REAL NOT NULL CHECK(amount >= 0),
                    description TEXT NOT NULL,
                    transaction_date TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL,
                    FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
                );

                CREATE TABLE IF NOT EXISTS budgets (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    category TEXT NOT NULL,
                    month_key TEXT NOT NULL,
                    target_amount REAL NOT NULL CHECK(target_amount >= 0),
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL,
                    UNIQUE(user_id, category, month_key),
                    FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
                );

                CREATE TABLE IF NOT EXISTS alert_log (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    alert_key TEXT NOT NULL,
                    message TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    UNIQUE(user_id, alert_key),
                    FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
                );
                """
            )

    def _hash_password(self, password: str, salt: str | None = None) -> tuple[str, str]:
        salt = salt or os.urandom(16).hex()
        digest = hashlib.pbkdf2_hmac(
            "sha256",
            password.encode("utf-8"),
            salt.encode("utf-8"),
            100_000,
        ).hex()
        return digest, salt

    def register_user(self, full_name: str, email: str, password: str) -> tuple[bool, str]:
        if not full_name.strip() or not email.strip() or not password:
            return False, "All fields are required."
        password_hash, salt = self._hash_password(password)
        now = datetime.utcnow().isoformat()
        try:
            with self.connect() as connection:
                cursor = connection.execute(
                    """
                    INSERT INTO users (full_name, email, password_hash, password_salt, created_at)
                    VALUES (?, ?, ?, ?, ?)
                    """,
                    (full_name.strip(), email.strip().lower(), password_hash, salt, now),
                )
                connection.execute(
                    """
                    INSERT INTO settings (user_id, email_address)
                    VALUES (?, ?)
                    """,
                    (cursor.lastrowid, email.strip().lower()),
                )
        except sqlite3.IntegrityError:
            return False, "An account with that email already exists."
        return True, "Account created. You can sign in now."

    def authenticate(self, email: str, password: str) -> dict[str, Any] | None:
        with self.connect() as connection:
            user = connection.execute(
                "SELECT * FROM users WHERE email = ?",
                (email.strip().lower(),),
            ).fetchone()
        if not user:
            return None
        hashed, _salt = self._hash_password(password, user["password_salt"])
        if hashed != user["password_hash"]:
            return None
        return user

    def update_user_name(self, user_id: int, full_name: str) -> None:
        with self.connect() as connection:
            connection.execute(
                "UPDATE users SET full_name = ? WHERE id = ?",
                (full_name.strip(), user_id),
            )

    def update_password(self, user_id: int, password: str) -> None:
        password_hash, salt = self._hash_password(password)
        with self.connect() as connection:
            connection.execute(
                """
                UPDATE users
                SET password_hash = ?, password_salt = ?
                WHERE id = ?
                """,
                (password_hash, salt, user_id),
            )

    def delete_user(self, user_id: int) -> None:
        with self.connect() as connection:
            connection.execute("DELETE FROM users WHERE id = ?", (user_id,))

    def get_settings(self, user_id: int) -> dict[str, Any]:
        with self.connect() as connection:
            settings = connection.execute(
                "SELECT * FROM settings WHERE user_id = ?",
                (user_id,),
            ).fetchone()
        return settings or {
            "user_id": user_id,
            "notifications_enabled": 1,
            "email_alerts_enabled": 0,
            "email_address": "",
            "currency": "USD",
            "theme": "Light",
        }

    def update_settings(
        self,
        user_id: int,
        notifications_enabled: bool,
        email_alerts_enabled: bool,
        email_address: str,
        currency: str,
        theme: str,
    ) -> None:
        with self.connect() as connection:
            connection.execute(
                """
                INSERT INTO settings (
                    user_id, notifications_enabled, email_alerts_enabled, email_address, currency, theme
                ) VALUES (?, ?, ?, ?, ?, ?)
                ON CONFLICT(user_id) DO UPDATE SET
                    notifications_enabled = excluded.notifications_enabled,
                    email_alerts_enabled = excluded.email_alerts_enabled,
                    email_address = excluded.email_address,
                    currency = excluded.currency,
                    theme = excluded.theme
                """,
                (
                    user_id,
                    int(notifications_enabled),
                    int(email_alerts_enabled),
                    email_address.strip(),
                    currency,
                    theme,
                ),
            )

    def list_transactions(self, user_id: int) -> list[dict[str, Any]]:
        with self.connect() as connection:
            return connection.execute(
                """
                SELECT * FROM transactions
                WHERE user_id = ?
                ORDER BY transaction_date DESC, id DESC
                """,
                (user_id,),
            ).fetchall()

    def save_transaction(
        self,
        user_id: int,
        transaction_type: str,
        category: str,
        amount: float,
        description: str,
        transaction_date: str,
        transaction_id: int | None = None,
    ) -> None:
        now = datetime.utcnow().isoformat()
        with self.connect() as connection:
            if transaction_id:
                connection.execute(
                    """
                    UPDATE transactions
                    SET transaction_type = ?, category = ?, amount = ?, description = ?,
                        transaction_date = ?, updated_at = ?
                    WHERE id = ? AND user_id = ?
                    """,
                    (
                        transaction_type,
                        category,
                        amount,
                        description.strip(),
                        transaction_date,
                        now,
                        transaction_id,
                        user_id,
                    ),
                )
            else:
                connection.execute(
                    """
                    INSERT INTO transactions (
                        user_id, transaction_type, category, amount, description,
                        transaction_date, created_at, updated_at
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        user_id,
                        transaction_type,
                        category,
                        amount,
                        description.strip(),
                        transaction_date,
                        now,
                        now,
                    ),
                )

    def delete_transaction(self, user_id: int, transaction_id: int) -> None:
        with self.connect() as connection:
            connection.execute(
                "DELETE FROM transactions WHERE id = ? AND user_id = ?",
                (transaction_id, user_id),
            )

    def get_transaction(self, user_id: int, transaction_id: int) -> dict[str, Any] | None:
        with self.connect() as connection:
            return connection.execute(
                "SELECT * FROM transactions WHERE id = ? AND user_id = ?",
                (transaction_id, user_id),
            ).fetchone()

    def upsert_budget(self, user_id: int, category: str, month_key: str, target_amount: float) -> None:
        now = datetime.utcnow().isoformat()
        with self.connect() as connection:
            connection.execute(
                """
                INSERT INTO budgets (user_id, category, month_key, target_amount, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?)
                ON CONFLICT(user_id, category, month_key) DO UPDATE SET
                    target_amount = excluded.target_amount,
                    updated_at = excluded.updated_at
                """,
                (user_id, category, month_key, target_amount, now, now),
            )

    def list_budgets(self, user_id: int, month_key: str) -> list[dict[str, Any]]:
        with self.connect() as connection:
            return connection.execute(
                """
                SELECT
                    b.category,
                    b.month_key,
                    b.target_amount,
                    COALESCE(SUM(
                        CASE
                            WHEN t.transaction_type = 'expense'
                                 AND substr(t.transaction_date, 1, 7) = b.month_key
                                 AND t.category = b.category
                            THEN t.amount
                            ELSE 0
                        END
                    ), 0) AS spent_amount
                FROM budgets b
                LEFT JOIN transactions t ON t.user_id = b.user_id
                WHERE b.user_id = ? AND b.month_key = ?
                GROUP BY b.category, b.month_key, b.target_amount
                ORDER BY b.category
                """,
                (user_id, month_key),
            ).fetchall()

    def get_dashboard_data(self, user_id: int) -> dict[str, Any]:
        month_key = date.today().strftime("%Y-%m")
        with self.connect() as connection:
            month_totals = connection.execute(
                """
                SELECT
                    COALESCE(SUM(CASE WHEN transaction_type = 'income' THEN amount END), 0) AS income_total,
                    COALESCE(SUM(CASE WHEN transaction_type = 'expense' THEN amount END), 0) AS expense_total
                FROM transactions
                WHERE user_id = ? AND substr(transaction_date, 1, 7) = ?
                """,
                (user_id, month_key),
            ).fetchone()

            category_rows = connection.execute(
                """
                SELECT category, ROUND(SUM(amount), 2) AS total
                FROM transactions
                WHERE user_id = ? AND transaction_type = 'expense'
                  AND substr(transaction_date, 1, 7) = ?
                GROUP BY category
                ORDER BY total DESC
                """,
                (user_id, month_key),
            ).fetchall()

            recent_transactions = connection.execute(
                """
                SELECT transaction_type, category, amount, description, transaction_date
                FROM transactions
                WHERE user_id = ?
                ORDER BY transaction_date DESC, id DESC
                LIMIT 8
                """,
                (user_id,),
            ).fetchall()

            trend_rows = connection.execute(
                """
                SELECT
                    substr(transaction_date, 1, 7) AS month_key,
                    ROUND(SUM(CASE WHEN transaction_type = 'income' THEN amount END), 2) AS income_total,
                    ROUND(SUM(CASE WHEN transaction_type = 'expense' THEN amount END), 2) AS expense_total
                FROM transactions
                WHERE user_id = ?
                GROUP BY substr(transaction_date, 1, 7)
                ORDER BY month_key DESC
                LIMIT 6
                """,
                (user_id,),
            ).fetchall()

        budgets = self.list_budgets(user_id, month_key)
        alerts = []
        for budget in budgets:
            if budget["target_amount"] <= 0:
                continue
            ratio = budget["spent_amount"] / budget["target_amount"]
            if ratio >= 1:
                alerts.append(
                    f"{budget['category']} budget exceeded by {budget['spent_amount'] - budget['target_amount']:.2f}"
                )
            elif ratio >= 0.9:
                alerts.append(f"{budget['category']} budget is above 90% used.")

        income_total = float(month_totals["income_total"] or 0)
        expense_total = float(month_totals["expense_total"] or 0)
        net = income_total - expense_total
        savings_ratio = 0 if income_total <= 0 else max(net, 0) / income_total
        adherence = 1.0
        if budgets:
            adherence = max(
                0.0,
                1 - (
                    sum(max(item["spent_amount"] - item["target_amount"], 0) for item in budgets)
                    / max(sum(item["target_amount"] for item in budgets), 1)
                ),
            )
        tracking_points = min(len(recent_transactions), 8) / 8
        financial_score = int(max(0, min(100, round((savings_ratio * 45 + adherence * 40 + tracking_points * 15) * 100))))

        return {
            "month_key": month_key,
            "income_total": income_total,
            "expense_total": expense_total,
            "net_total": net,
            "financial_score": financial_score,
            "category_breakdown": category_rows,
            "recent_transactions": recent_transactions,
            "monthly_trends": list(reversed(trend_rows)),
            "alerts": alerts,
        }

    def get_dashboard_data_for_month(self, user_id: int, month_key: str) -> dict[str, Any]:
        with self.connect() as connection:
            month_totals = connection.execute(
                """
                SELECT
                    COALESCE(SUM(CASE WHEN transaction_type = 'income' THEN amount END), 0) AS income_total,
                    COALESCE(SUM(CASE WHEN transaction_type = 'expense' THEN amount END), 0) AS expense_total
                FROM transactions
                WHERE user_id = ? AND substr(transaction_date, 1, 7) = ?
                """,
                (user_id, month_key),
            ).fetchone()

            transactions = connection.execute(
                """
                SELECT *
                FROM transactions
                WHERE user_id = ? AND substr(transaction_date, 1, 7) = ?
                ORDER BY transaction_date DESC, id DESC
                """,
                (user_id, month_key),
            ).fetchall()
        income_total = float(month_totals["income_total"] or 0)
        expense_total = float(month_totals["expense_total"] or 0)
        return {
            "income_total": income_total,
            "expense_total": expense_total,
            "net_total": income_total - expense_total,
            "transactions": transactions,
        }

    def get_stats_breakdown(self, user_id: int, transaction_type: str) -> list[dict[str, Any]]:
        with self.connect() as connection:
            rows = connection.execute(
                """
                SELECT category, ROUND(SUM(amount), 2) AS total
                FROM transactions
                WHERE user_id = ? AND transaction_type = ?
                GROUP BY category
                ORDER BY total DESC
                """,
                (user_id, transaction_type),
            ).fetchall()
        return rows

    def log_alerts(self, user_id: int, messages: list[str], email_address: str) -> int:
        if not messages:
            return 0
        sent_count = 0
        with self.connect() as connection:
            for message in messages:
                alert_key = hashlib.sha1(message.encode("utf-8")).hexdigest()
                try:
                    connection.execute(
                        """
                        INSERT INTO alert_log (user_id, alert_key, message, created_at)
                        VALUES (?, ?, ?, ?)
                        """,
                        (user_id, alert_key, message, datetime.utcnow().isoformat()),
                    )
                except sqlite3.IntegrityError:
                    continue
                OUTBOX_PATH.parent.mkdir(parents=True, exist_ok=True)
                with OUTBOX_PATH.open("a", encoding="utf-8") as outbox:
                    outbox.write(f"[{datetime.utcnow().isoformat()}] To: {email_address or 'not-set'} | {message}\n")
                sent_count += 1
        return sent_count
