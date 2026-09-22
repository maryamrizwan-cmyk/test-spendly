# Spec: Registration

## Overview
Implements account creation for Spendly. `templates/register.html` already exists and POSTs `name`, `email`, and `password` to `/register`, but the route only handles GET and renders the template with no processing — submissions currently 405. This step replaces that placeholder with a real `POST /register` handler that validates input, hashes the password, inserts a new row into `users`, and sends the new user to `/login` to sign in. No session or "logged in" state is introduced here — that belongs to the login/logout step.

## Depends on
Step 1 (database setup) — requires `get_db()` and the `users` table (`id`, `name`, `email` UNIQUE, `password_hash`, `created_at`) from `database/db.py`.

## Routes
- `GET /register` — render the registration form — public (already exists, unchanged)
- `POST /register` — validate submitted form data, create the user, redirect to login — public

## Database changes
No database changes. `users` table already has everything needed (`email UNIQUE` gives duplicate-account protection at the DB level).

## Templates
- **Create:** none
- **Modify:** `templates/register.html` — no structural change; it already renders `{{ error }}` into `.auth-error`. On a validation failure the route re-renders this template passing `error`.

## Files to change
- `app.py` — change `/register` to `methods=["GET", "POST"]`; on POST, validate the form, hash the password with `werkzeug.security.generate_password_hash`, insert the user via a parameterised query, and redirect to `url_for('login')` on success.

## Files to create
None.

## New dependencies
No new dependencies.

## Rules for implementation
- No SQLAlchemy or ORMs
- Parameterised queries only
- Passwords hashed with werkzeug (`generate_password_hash(password, method="pbkdf2")`, matching the method already used in `seed_db()`)
- Use CSS variables — never hardcode hex values
- All templates extend `base.html`
- Validate server-side even though the form has `required`/`type="email"` — name and email must be non-empty, email must contain `@`, password must be at least 8 characters
- On duplicate email, missing field, or short password, re-render `register.html` with a specific `error` message and the submitted `name`/`email` preserved in the form (not the password)
- Do not create a session, set cookies, or add any "logged in" concept — that is out of scope for this step
- Do not touch `/login`, `/logout`, `/profile`, or the expense routes

## Definition of done
- [ ] `GET /register` still renders the form exactly as before
- [ ] Submitting valid name/email/password creates a new row in `users` with a hashed (not plaintext) password
- [ ] After successful registration, the browser is redirected to `/login`
- [ ] Submitting an email that already exists re-renders `register.html` with an error and does not insert a duplicate row
- [ ] Submitting with a missing name, missing email, or missing password re-renders the form with an error
- [ ] Submitting a password under 8 characters re-renders the form with an error
- [ ] The app starts and runs with no errors (`python app.py`)
