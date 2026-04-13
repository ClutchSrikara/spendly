# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**Spendly** — a Flask-based expense tracker web app designed as a step-by-step teaching project. Students incrementally build authentication and expense CRUD features. Many routes in `app.py` are placeholders awaiting implementation.

## Commands

```bash
# Activate virtual environment (required before running anything)
source venv/bin/activate

# Run the dev server (port 5001, debug mode)
python app.py

# Run all tests
pytest

# Run a single test file
pytest tests/test_something.py -v
```

## Architecture

- **`app.py`** — Single-file Flask app with all routes. No blueprints; routes are defined directly on the `app` object.
- **`database/db.py`** — Database module (SQLite). Students implement `get_db()`, `init_db()`, and `seed_db()`. Currently a stub with comments.
- **`templates/`** — Jinja2 templates extending `base.html`. The base template provides navbar, footer, and block structure (`title`, `head`, `content`, `scripts`).
- **`static/css/`** — `style.css` (global) and `landing.css` (landing page specific).
- **`static/js/main.js`** — Shared JavaScript file, currently a stub.

## Key Details

- The app name displayed in UI is **Spendly** (brand icon: ◈).
- Templates use Google Fonts: DM Serif Display and DM Sans.
- The project uses `werkzeug` for password hashing (listed in requirements but not yet wired up).
- SQLite database with foreign keys enabled (per db.py comments).
- Currency context is Indian Rupees (₹) based on the footer copy.
