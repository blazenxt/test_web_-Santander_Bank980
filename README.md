# Blaze NXT - Enterprise OTP Dashboard

This repository contains the backend and dashboard interface for the Blaze NXT Enterprise OTP Dashboard.

## Files
- `app.py`: The Telegram Bot daemon, which manages OTP processing and queues.
- `dashboard.py`: Flask-based REST API and backend serving data to the web dashboard.
- `dashboard.html`: Single-page application containing the admin interface for data visualization.
- `.env`: A generated environment configurations file.

## Environment variables (.env)
The newly created `.env` file ensures the JWT secret, Telegram bot token, and server ports are correctly established.

```env
BOT_TOKEN=8844128671:AAFRLGcU9ns8QRje_AjMU1uKsFhXxHEDzbo
DASHBOARD_PASS=admin123
DASHBOARD_SECRET=supersecretkey_for_jwt_auth_123456
DASHBOARD_PORT=8080
OWNER_IDS=8708907310,8726642457,5618954306,6059791675
```

---

## Complete Bug Analysis

### 1. `app.py`
- **Dictionary vs List Typo (Fixed):**
  `DEFAULT_PANELS` was initially instantiated as an empty list `[]`. The actual dictionary declaration `{ "BLAZENXT PANEL": {...} }` was mistakenly disabled by being wrapped in a multi-line comment `"""`. This resulted in an `AttributeError` when `API_PANELS.keys()` was queried downstream. *Fix applied directly to the file.*
- **Event Loop Blocking Issue (Fixed):**
  The async bot handler `fetchsms_command` called `fetch_all_panels(limit=5)` directly. `fetch_all_panels` uses synchronous I/O operations (`requests.get()`) without timing out asynchronously. This effectively halts the `asyncio` event loop, making the bot unresponsive to other users until all panels fetch operations are completed. *Fixed by wrapping it in `asyncio.get_running_loop().run_in_executor()`.*

### 2. `dashboard.py`
- **Database Dependency Order / Crash Risk:**
  `dashboard.py` utilizes SQLite queries (via the `get_db()` helper) against tables like `tg_users` and `numbers`. However, it doesn't initialize these tables. If `dashboard.py` boots prior to `app.py` completing its initial SQLite `CREATE TABLE IF NOT EXISTS` setup, `dashboard.py` will crash internally (`sqlite3.OperationalError`). 
- **Secret Hardcoding Security Threat:**
  The `DASHBOARD_SECRET` defaults to `"changeme_secret_32chars_minimum!"`. Without an `.env` specification or runtime secret generator, a hacker who knows the source code default can mint unauthorized `is_owner: true` JSON Web Tokens (JWTs) and take full control of the backend system.

### 3. `dashboard.html`
- **XSS (Cross-Site Scripting) Injection Points:**
  The Javascript extensively assigns properties to the DOM via `.innerHTML` directly connected to mapped API variables (`panels`, `broadcast history`, etc). E.g., `Object.entries(panels).map(([name, p]) => \`<div class="...">${name}</div>...\`)`. Should a compromised or malicious user input a `<script>` or event-based tag (e.g., `<img src='x' onerror='alert(1)'>`) for a panel name or URL, it will inject Javascript into any user's browser reading the dashboard.
- **Copy-to-Clipboard Security Fallback:**
  The `fallbackCopyTextToClipboard` appends a text area directly to the body and runs `document.execCommand('copy')`. In modern contexts, it doesn't gracefully revert or hide visual jumps due to `textarea` layout shift on mobile, potentially causing focus layout bugs on older iOS devices.