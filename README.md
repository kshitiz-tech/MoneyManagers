# Money Manager

Money Manager is a full-stack budgeting application built with Python, Kivy, and SQLite. It implements the final-project scope from `MoneyManagers_ProjectFeatures-1-1.pdf` and mirrors the supplied `Create All Pages` mobile UI with Kivy screens.

## Technologies and Versions

- Python 3.11
- Kivy 2.3.0
- SQLite 3
- Docker / Docker Compose
- noVNC + Xvfb for browser-based access to the Kivy desktop UI

## Project Structure

- `main.py`: app entry point
- `money_manager/`: application package
- `docs/architecture.md`: concise technical overview
- `Dockerfile`: container image
- `docker-compose.yml`: local run configuration
- `data/`: runtime SQLite database and generated alert outbox

## Implemented Pages

The app contains exactly seven pages derived from the supplied `Create All Pages` design:

1. Login
2. Register
3. Dashboard
4. Transaction
5. Budget Planning
6. Statistics
7. Profile

## Features Implemented

- User registration and login with salted password hashing
- Persistent SQLite user, transaction, budget, and settings storage
- Income and expense CRUD workflow
- Dashboard metrics for monthly income, expense, net balance, and financial score
- Visual dashboard sections for category spending and monthly trends
- Overspending alerts based on budget thresholds
- Email reminder preview written to `data/outbox.log`
- Budget planning by category and month
- Statistics page with income and expense category breakdown
- Profile page with settings for notifications, email reminders, currency, and theme

## How to Run

### Preferred Method: Docker

1. From the project root, build and start the container:

```bash
docker compose up --build
```

2. Wait for the app to start, then open:

```text
http://localhost:6080/vnc.html
```

3. The Kivy application window will appear inside the browser through noVNC.

4. To stop the application:

```bash
docker compose down
```

## Local Development Run

If Docker is not required for your environment and you already have Kivy installed:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python main.py
```

## Initial Use

1. Open the Login page or move to Register.
2. Register a new account.
3. Sign in with that account.
4. Add or edit entries from the Transaction page.
5. Add monthly category budgets on the Budget page.
6. Review totals on the Dashboard page.
7. Review category breakdowns on the Statistics page.
8. Save preferences on the Profile page.

## Notes for Grading

- Runtime data is stored in `data/money_manager.db`.
- Email reminders are represented by lines appended to `data/outbox.log` whenever new overspending alerts are triggered and email reminders are enabled.
- The UI is intentionally simple and professional to keep the deliverable easy to run and review.
