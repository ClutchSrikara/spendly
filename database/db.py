import sqlite3
import os
from werkzeug.security import generate_password_hash


DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "spendly.db")


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    db = get_db()
    db.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TEXT DEFAULT (datetime('now'))
        )
    """)
    db.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL REFERENCES users(id),
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            date TEXT NOT NULL,
            description TEXT,
            created_at TEXT DEFAULT (datetime('now'))
        )
    """)
    db.commit()
    db.close()


def seed_db():
    db = get_db()
    count = db.execute("SELECT COUNT(*) FROM users").fetchone()[0]
    if count > 0:
        db.close()
        return

    db.execute(
        "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
        ("Demo User", "demo@spendly.com", generate_password_hash("demo123", method="pbkdf2:sha256")),
    )
    user_id = db.execute("SELECT id FROM users WHERE email = ?", ("demo@spendly.com",)).fetchone()[0]

    expenses = [
        (user_id, 250.00, "Food", "2026-04-01", "Lunch at cafe"),
        (user_id, 150.00, "Transport", "2026-04-03", "Auto to office"),
        (user_id, 1200.00, "Bills", "2026-04-05", "Electricity bill"),
        (user_id, 500.00, "Health", "2026-04-07", "Pharmacy"),
        (user_id, 350.00, "Entertainment", "2026-04-09", "Movie tickets"),
        (user_id, 800.00, "Shopping", "2026-04-11", "New headphones"),
        (user_id, 100.00, "Other", "2026-04-12", "Stationery"),
        (user_id, 450.00, "Food", "2026-04-13", "Dinner with friends"),
    ]
    db.executemany(
        "INSERT INTO expenses (user_id, amount, category, date, description) VALUES (?, ?, ?, ?, ?)",
        expenses,
    )
    db.commit()
    db.close()
