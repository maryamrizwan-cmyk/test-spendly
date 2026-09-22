# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

Spendly — a Flask expense tracker built as a **step-by-step teaching scaffold**. The landing/auth/legal pages are done; the actual expense-tracking features are deliberately unimplemented. `app.py` has placeholder routes annotated with the step that implements them (`/logout` → Step 3, `/profile` → Step 4, `/expenses/add` → Step 7, edit → Step 8, delete → Step 9), and `database/db.py` is a comment-only stub specifying the three functions it must eventually export: `get_db()` (SQLite connection with `row_factory` and foreign keys on), `init_db()` (`CREATE TABLE IF NOT EXISTS`), `seed_db()`.

When asked for a feature, implement only that step's scope — replacing a placeholder route is expected, but don't opportunistically fill in other placeholders or write `db.py` unless the request covers it.

## Commands

```bash
source venv/bin/activate          # Python 3.9 venv is committed-adjacent but gitignored
pip install -r requirements.txt
python app.py                     # http://localhost:5001 (not 5000), debug=True
```

`pytest` and `pytest-flask` are in requirements but there are no tests yet. Once tests exist: `pytest`, single test `pytest tests/test_x.py::test_name`. No linter, formatter, or build step is configured.

## Architecture and conventions

**No build tooling, no JS framework, no CSS framework.** Everything is server-rendered Jinja2 plus static assets served directly by Flask. Do not introduce npm, a bundler, Tailwind, Bootstrap, or a JS library — vanilla JS only.

- `app.py` — single module, all routes, no blueprints. Routes are grouped under banner comments (`# Routes` / `# Placeholder routes`).
- `templates/base.html` — every page does `{% extends "base.html" %}` and fills `{% block title %}`, `{% block content %}`, and optionally `{% block head %}` / `{% block scripts %}`. The navbar and footer live here, so a site-wide link change is a one-file edit.
- `static/css/style.css` — one stylesheet for the whole app, ~680 lines, organized by banner-comment sections (Variables, Reset, Navbar, Hero, …). Colors, fonts, radii, and widths are CSS custom properties in `:root`; use the existing tokens (`--ink`, `--paper`, `--accent`, `--radius-md`, …) instead of literal values, and add new rules to the matching section rather than the end of the file.
- `static/js/main.js` — loaded on every page, currently empty; reserved for shared behavior. Page-specific JS goes inline in that page's `{% block scripts %}`, wrapped in an IIFE (see the video modal in `templates/landing.html`).
- Internal links use `{{ url_for('<endpoint>') }}`, never hardcoded paths. (Form `action` attributes are currently literal strings — `url_for` is preferred for new forms.)
- **Every route is GET-only** — no `@app.route` declares `methods=`. `login.html` and `register.html` already POST to `/login` and `/register`, so those submissions 405 until the step that implements auth adds `methods=["GET", "POST"]`. The same applies to the expense add/edit/delete placeholders, which should take POST rather than mutating on a GET.
- Currency throughout the UI is Indian rupees (₹).
- Templates render an `{{ error }}` string into `.auth-error` when present; the auth views don't pass it yet.

## Git

Commit subjects follow `<area>: <lowercase summary>`, e.g. `landing: add privacy policy page and route`. Current branch is `feature-a`; PRs target `main`.

Note: `static/css/Add two links to the footer in @template` is a stray untracked file containing prompt text, not source. Ignore it, and don't create files from unquoted prompt text.
