from __future__ import annotations

from datetime import date, datetime
from typing import Any

from money_manager.database import CATEGORIES, CURRENCIES, THEMES, Database


class MoneyManagerService:
    def __init__(self, db: Database) -> None:
        self.db = db

    def register(self, name: str, email: str, password: str) -> tuple[bool, str]:
        return self.db.register_user(name, email, password)

    def login(self, email: str, password: str) -> dict[str, Any] | None:
        return self.db.authenticate(email, password)

    def update_profile_name(self, user_id: int, full_name: str) -> tuple[bool, str]:
        if not full_name.strip():
            return False, "Name is required."
        self.db.update_user_name(user_id, full_name)
        return True, "Name updated."

    def change_password(self, user_id: int, password: str, confirm_password: str) -> tuple[bool, str]:
        if len(password) < 6:
            return False, "Password must be at least 6 characters."
        if password != confirm_password:
            return False, "Passwords do not match."
        self.db.update_password(user_id, password)
        return True, "Password changed."

    def save_transaction(
        self,
        user_id: int,
        transaction_type: str,
        category: str,
        amount_text: str,
        description: str,
        transaction_date: str,
        transaction_id: int | None = None,
    ) -> tuple[bool, str]:
        if transaction_type not in {"income", "expense"}:
            return False, "Select a valid transaction type."
        if category not in CATEGORIES:
            return False, "Select a valid category."
        if not description.strip():
            return False, "Description is required."
        try:
            amount = float(amount_text)
        except ValueError:
            return False, "Amount must be numeric."
        if amount <= 0:
            return False, "Amount must be greater than zero."
        try:
            datetime.strptime(transaction_date, "%Y-%m-%d")
        except ValueError:
            return False, "Use date format YYYY-MM-DD."
        self.db.save_transaction(
            user_id,
            transaction_type,
            category,
            amount,
            description,
            transaction_date,
            transaction_id,
        )
        return True, "Transaction saved."

    def save_budget(self, user_id: int, category: str, amount_text: str, month_key: str) -> tuple[bool, str]:
        if category not in CATEGORIES:
            return False, "Select a valid category."
        try:
            amount = float(amount_text)
        except ValueError:
            return False, "Budget amount must be numeric."
        if amount < 0:
            return False, "Budget amount cannot be negative."
        try:
            datetime.strptime(month_key + "-01", "%Y-%m-%d")
        except ValueError:
            return False, "Use month format YYYY-MM."
        self.db.upsert_budget(user_id, category, month_key, amount)
        return True, "Budget updated."

    def save_settings(
        self,
        user_id: int,
        notifications_enabled: bool,
        email_alerts_enabled: bool,
        email_address: str,
        currency: str,
        theme: str,
    ) -> tuple[bool, str]:
        if currency not in CURRENCIES:
            return False, "Select a valid currency."
        if theme not in THEMES:
            return False, "Select a valid theme."
        if email_alerts_enabled and not email_address.strip():
            return False, "Email address is required when email alerts are enabled."
        self.db.update_settings(
            user_id,
            notifications_enabled,
            email_alerts_enabled,
            email_address,
            currency,
            theme,
        )
        return True, "Settings saved."

    def default_transaction_date(self) -> str:
        return date.today().isoformat()

    def default_budget_month(self) -> str:
        return date.today().strftime("%Y-%m")
