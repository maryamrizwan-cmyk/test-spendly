import sqlite3
from contextlib import closing
from datetime import date
from pathlib import Path

from werkzeug.security import generate_password_hash

# The database lives in the project root, one level up from this package.
DB_PATH = Path(__file__).resolve().parent.parent / "expense_tracker.db"

# Fixed category list used across the app.
CATEGORIES = (
    "Food",
    "Transport",
    "Bills",
    "Health",
    "Entertainment",
    "Shopping",
    "Other",
)


def get_db():
    """Return a SQLite connection with dict-like rows and foreign keys on."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    # Per-connection pragma — SQLite silently ignores FK violations without it.
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    """Create the tables if they don't exist. Safe to call repeatedly."""
    with closing(get_db()) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id            INTEGER PRIMARY KEY AUTOINCREMENT,
                name          TEXT NOT NULL,
                email         TEXT NOT NULL UNIQUE,
                password_hash TEXT NOT NULL,
                created_at    TEXT NOT NULL DEFAULT (datetime('now'))
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS expenses (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id     INTEGER NOT NULL REFERENCES users(id),
                amount      REAL NOT NULL,
                category    TEXT NOT NULL,
                date        TEXT NOT NULL,
                description TEXT,
                created_at  TEXT NOT NULL DEFAULT (datetime('now'))
            )
            """
        )
        conn.commit()


def seed_db():
    """Insert demo data once. Does nothing if any user already exists."""
    with closing(get_db()) as conn:
        if conn.execute("SELECT 1 FROM users LIMIT 1").fetchone() is not None:
            return

        cur = conn.execute(
            "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
            (
                "Demo User",
                "demo@spendly.com",
                # pbkdf2, not the werkzeug default scrypt — this Python build
                # has no hashlib.scrypt.
                generate_password_hash("demo123", method="pbkdf2"),
            ),
        )
        user_id = cur.lastrowid

        # Days stay at 28 or below so every date is valid in February too.
        def day(n):
            return date.today().replace(day=n).isoformat()

        conn.executemany(
            """
            INSERT INTO expenses (user_id, amount, category, date, description)
            VALUES (?, ?, ?, ?, ?)
            """,
            [
                (user_id, 450.0, "Food", day(2), "Groceries for the week"),
                (user_id, 120.5, "Transport", day(4), "Auto rickshaw to office"),
                (user_id, 1899.0, "Bills", day(7), "Electricity bill"),
                (user_id, 650.0, "Health", day(10), "Pharmacy refill"),
                (user_id, 499.0, "Entertainment", day(14), "Movie tickets"),
                (user_id, 2250.75, "Shopping", day(18), "Running shoes"),
                (user_id, 300.0, "Other", day(22), "Gift for a friend"),
                (user_id, 180.0, "Food", day(25), "Lunch with colleagues"),
            ],
        )
        conn.commit()
