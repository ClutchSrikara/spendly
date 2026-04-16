# Spec: Registration

## Overview
Wire up user registration so new visitors can create a Spendly account. The `register.html` template and `GET /register` route already render the form; this step adds the `POST /register` handler that validates input, hashes the password with werkzeug, inserts a new row into the `users` table, and logs the new user in via Flask session before redirecting them into the app. This is the first interactive feature built on top of the database layer from step 01 and is a prerequisite for login, profile, and every expense route.

## Depends on
- Step 01 — Database setup (the `users` table, `get_db()`, and `init_db()` must already exist).

## Routes
- `GET /register` — renders the registration form — public. Already exists; must remain functional.
- `POST /register` — accepts form submission, creates the user, starts a session, redirects to `/profile` — public.

## Database changes
No database changes. The existing `users` table from step 01 (`id`, `name`, `email`, `password_hash`, `created_at`) is sufficient.

## Templates
- **Create:** none.
- **Modify:** `templates/register.html` — ensure the existing `{% if error %}` block is used to surface server-side validation errors (already scaffolded; confirm no changes required beyond verifying field names `name`, `email`, `password` match the handler).

## Files to change
- `app.py` — convert the `register` route to accept both `GET` and `POST`, add validation, insertion, and session login logic. Import `request`, `redirect`, `url_for`, `session` from Flask and `generate_password_hash` from `werkzeug.security`. Configure `app.secret_key` so sessions work.
- `templates/register.html` — only if field names or error rendering need to be tightened to match the handler.

## Files to create
None.

## New dependencies
No new dependencies. `werkzeug` (for `generate_password_hash`) and Flask's built-in `session` are already available.

## Rules for implementation
- No SQLAlchemy or ORMs — use the `get_db()` helper and raw SQL.
- Parameterised queries only — never interpolate user input into SQL strings.
- Passwords must be hashed with `werkzeug.security.generate_password_hash` using `method="pbkdf2:sha256"` (matches `seed_db()`). Never store plaintext.
- Use CSS variables from `static/css/style.css` — never hardcode hex values in any template or stylesheet change.
- All templates extend `base.html`.
- Single-file Flask app — keep the new logic in `app.py`, no blueprints.
- Validate on the server even though the form has `required`: trim whitespace, require non-empty `name`, a syntactically plausible `email` (contains `@`), and a password of at least 8 characters. Re-render `register.html` with an `error` message on failure — never raise an uncaught exception to the user.
- Handle the `sqlite3.IntegrityError` from the `UNIQUE` constraint on `email` and show a friendly "An account with that email already exists." message instead of a stack trace.
- Always close the DB connection (use `try/finally` or a context manager).
- On success, store `session["user_id"]` and `session["user_name"]`, then `redirect(url_for("profile"))`.
- `app.secret_key` must be read from an environment variable (e.g. `FLASK_SECRET_KEY`) with a safe dev fallback — do not commit a production secret.

## Definition of done
- [ ] Visiting `/register` still renders the existing form with no regressions.
- [ ] Submitting a valid new name/email/password creates exactly one row in `users` with a hashed (non-plaintext) `password_hash`.
- [ ] After successful registration the browser is redirected to `/profile` and `session["user_id"]` is populated.
- [ ] Submitting an email that already exists re-renders `/register` with a visible error and does not create a second row.
- [ ] Submitting an empty name, malformed email, or password shorter than 8 characters re-renders `/register` with a specific error and does not hit the database.
- [ ] All inserts use parameterised SQL (verified by code inspection — no f-strings or `%` formatting in queries).
- [ ] `app.secret_key` is set; sessions survive a page reload.
- [ ] `python app.py` starts cleanly on port 5001 with no new warnings.
