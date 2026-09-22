# Spec: Login and Logout

## Overview
Implements sign-in and sign-out for Spendly. `templates/login.html` already exists and POSTs `email` and `password` to `/login`, but the route only handles GET — submissions currently 405. `/logout` is a placeholder string response. This step replaces both with real handlers: `POST /login` validates credentials against the `users` table and starts a Flask session; `/logout` clears that session and sends the user back to the landing page. The navbar in `base.html` is updated to reflect signed-in state so there is a visible way to log out. No route protection (redirecting anonymous users away from `/profile` or the expense routes) is introduced here — that belongs to whichever later step actually implements those pages.

## Depends on
- Step 1 (database setup) — requires `get_db()` and the `users` table (`id`, `name`, `email` UNIQUE, `password_hash`) from `database/db.py`.
- Step 2 (registration) — requires `POST /register` to exist so accounts can be created with hashed passwords to log in against.

## Routes
- `GET /login` — render the sign-in form — public (already exists, unchanged)
- `POST /login` — validate email/password against `users`, start a session, redirect to `/` — public
- `GET|POST /logout` — clear the session, redirect to `/` — logged-in (currently a GET-only placeholder; change to accept the same methods and clear session state)

## Database changes
No database changes. `users` table already has everything needed (`email`, `password_hash`).

## Templates
- **Create:** none
- **Modify:**
  - `templates/login.html` — no structural change; it already renders `{{ error }}` into `.auth-error`. On a failed login the route re-renders this template passing `error`.
  - `templates/base.html` — navbar `nav-links` block becomes conditional: when a session user is present, show the user's name (static text, not a link — `/profile` isn't implemented yet) and a "Logout" link to `url_for('logout')`; when absent, show the existing "Sign in" / "Get started" links unchanged.

## Files to change
- `app.py`:
  - Set `app.secret_key` (required for Flask sessions) — read from an environment variable with a hardcoded local-dev fallback, e.g. `os.environ.get("SECRET_KEY", "dev-only-not-for-production")`.
  - Change `/login` to `methods=["GET", "POST"]`; on POST, look up the user by email, verify the password with `werkzeug.security.check_password_hash`, store `session["user_id"]` and `session["user_name"]` on success, and redirect to `url_for('landing')`.
  - Change `/logout` from the placeholder string to a real handler with `methods=["GET", "POST"]` that calls `session.clear()` and redirects to `url_for('landing')`.
- `templates/base.html` — wrap the `nav-links` markup in an `{% if session.get('user_id') %}` / `{% else %}` block as described above.

## Files to create
None.

## New dependencies
No new dependencies. Flask's built-in session (signed cookie, no `Flask-Login`/`Flask-Session` package) is sufficient here.

## Rules for implementation
- No SQLAlchemy or ORMs
- Parameterised queries only
- Passwords hashed with werkzeug — use `check_password_hash` against the existing `password_hash` column; do not re-hash or change how passwords are stored
- Use CSS variables — never hardcode hex values
- All templates extend `base.html`
- On an unknown email or wrong password, re-render `login.html` with a single generic error (e.g. "Invalid email or password.") — do not reveal whether the email exists
- Do not implement `/profile` or route-protection redirects — out of scope for this step
- Do not touch `/register` or the expense routes

## Definition of done
- [ ] `GET /login` still renders the form exactly as before
- [ ] Submitting a registered email with the correct password redirects to `/` and the navbar shows the logged-in state
- [ ] Submitting a wrong password or an email that doesn't exist re-renders `login.html` with a generic error and does not start a session
- [ ] Visiting `/logout` while logged in clears the session and redirects to `/`, and the navbar reverts to "Sign in" / "Get started"
- [ ] Visiting `/logout` while not logged in does not error — it just redirects to `/`
- [ ] The app starts and runs with no errors (`python app.py`)
