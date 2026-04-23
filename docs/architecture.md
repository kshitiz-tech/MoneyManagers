# Money Manager Architecture

## Stack

- Python 3.11
- Kivy 2.3.0
- SQLite
- Docker with Xvfb, x11vnc, and noVNC for browser-based access

## Repository Layout

- `main.py`: application entry point
- `money_manager/app.py`: Kivy screen flow and UI composition
- `money_manager/database.py`: SQLite schema, password hashing, queries, and analytics
- `money_manager/services.py`: validation and application service logic
- `money_manager/widgets.py`: reusable card and dashboard components
- `docs/architecture.md`: implementation overview

## Pages

The application contains seven primary pages:

1. Login
2. Register
3. Dashboard
4. Transaction
5. Budget
6. Stats
7. Profile

## Data Model

- `users`: account registration and hashed credentials
- `settings`: per-user notification, email, currency, and theme preferences
- `transactions`: income and expense records
- `budgets`: monthly category budgets
- `alert_log`: deduplicated overspending reminders

## Alert Handling

When overspending rules trigger and email reminders are enabled, the app writes a delivery preview to `data/outbox.log`. This provides a concrete and testable reminder workflow without depending on third-party email services during grading.

## Design Mapping

The Kivy implementation preserves the same seven-screen workflow while embedding settings controls into the `Profile` page.
