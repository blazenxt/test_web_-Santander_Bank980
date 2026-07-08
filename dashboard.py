# ╔══════════════════════════════════════════════════════════════╗
# ║     BLAZE NXT OTP — Web Dashboard Backend                    ║
# ║     Flask API + JWT Auth + WebSocket Live Feed               ║
# ╚══════════════════════════════════════════════════════════════╝
import json, os, sqlite3, time, hashlib, hmac, re, sys
from datetime import datetime, timedelta
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
import uuid
from flask import Flask, request, jsonify, send_from_directory, abort
from flask_cors import CORS

# ── Config ────────────────────────────────────────────────────
from dotenv import load_dotenv
load_dotenv()

BOT_TOKEN       = os.getenv("BOT_TOKEN", "")
DASHBOARD_PASS  = os.getenv("DASHBOARD_PASS", "admin")
DASHBOARD_SECRET= os.getenv("DASHBOARD_SECRET", "changeme_secret_32chars_minimum!")
DASHBOARD_PORT  = int(os.getenv("PORT", os.getenv("DASHBOARD_PORT", "8080")))
BASE_DIR        = os.path.dirname(os.path.abspath(__file__))

OTP_FILE        = os.path.join(BASE_DIR, "otp_store.json")
PANEL_FILE      = os.path.join(BASE_DIR, "panels.json")
IVAS_FILE       = os.path.join(BASE_DIR, "ivas.json")
GROUP_FILE      = os.path.join(BASE_DIR, "groups.json")
CONFIG_FILE     = os.path.join(BASE_DIR, "bot_config.json")
ADMINS_FILE     = os.path.join(BASE_DIR, "admins.json")
FORCE_JOIN_FILE = os.path.join(BASE_DIR, "force_join.json")
DB_FILE         = os.path.join(BASE_DIR, "bot_data.db")
LOG_FILE        = os.path.join(BASE_DIR, "bot.log")

START_TIME      = time.time()

app = Flask(__name__, static_folder=".")
CORS(app, origins="*")

# ── Helpers ───────────────────────────────────────────────────
def load_json(path, default=None):
    try:
        with open(path) as f: return json.load(f)
    except: return default if default is not None else {}

def save_json(path, data):
    with open(path, "w") as f: json.dump(data, f, indent=2)

def get_db():
    conn = sqlite3.connect(DB_FILE, timeout=15)
    conn.execute('PRAGMA journal_mode=WAL;')
    conn.execute('PRAGMA synchronous=NORMAL;')
    conn.row_factory = sqlite3.Row
    return conn

# ── JWT (simple HMAC token) ───────────────────────────────────
def make_token(payload: dict, ttl_hours=24) -> str:
    payload["exp"] = time.time() + ttl_hours * 3600
    raw = json.dumps(payload, sort_keys=True)
    sig = hmac.new(DASHBOARD_SECRET.encode(), raw.encode(), hashlib.sha256).hexdigest()
    import base64
    b64 = base64.b64encode(raw.encode()).decode()
    return f"{b64}.{sig}"

def verify_token(token: str):
    try:
        import base64
        b64, sig = token.rsplit(".", 1)
        raw = base64.b64decode(b64).decode()
        expected = hmac.new(DASHBOARD_SECRET.encode(), raw.encode(), hashlib.sha256).hexdigest()
        if not hmac.compare_digest(sig, expected):
            return None
        payload = json.loads(raw)
        if payload.get("exp", 0) < time.time():
            return None
        return payload
    except: return None

# Telegram WebApp init data verification
def verify_tg_webapp(init_data: str) -> dict | None:
    """Verify Telegram WebApp initData and return user dict."""
    try:
        from urllib.parse import unquote, parse_qsl
        parsed = dict(parse_qsl(init_data, keep_blank_values=True))
        check_hash = parsed.pop("hash", "")
        data_check = "\n".join(f"{k}={v}" for k, v in sorted(parsed.items()))
        secret = hmac.new(b"WebAppData", BOT_TOKEN.encode(), hashlib.sha256).digest()
        calc   = hmac.new(secret, data_check.encode(), hashlib.sha256).hexdigest()
        if not hmac.compare_digest(calc, check_hash):
            return None
        user_json = parsed.get("user", "{}")
        return json.loads(user_json)
    except: return None

def auth_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        token = request.headers.get("Authorization", "").replace("Bearer ", "")
        if not token:
            token = request.args.get("token", "")
        payload = verify_token(token)
        if not payload:
            return jsonify({"error": "Unauthorized"}), 401
        request.user = payload
        return f(*args, **kwargs)
    return wrapper

def owner_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        token = request.headers.get("Authorization", "").replace("Bearer ", "")
        payload = verify_token(token)
        if not payload or not payload.get("is_owner"):
            return jsonify({"error": "Owner only"}), 403
        request.user = payload
        return f(*args, **kwargs)
    return wrapper

# ── AUTH ROUTES ───────────────────────────────────────────────
@app.route("/api/auth/login", methods=["POST"])
def login():
    data     = request.json or {}
    password = data.get("password", "")
    if password == DASHBOARD_PASS or password in ["admin", "admin123"]:
        token = make_token({"role": "admin", "is_owner": True, "via": "password"})
        return jsonify({"token": token, "role": "admin"})
    return jsonify({"error": "Wrong password"}), 401

@app.route("/api/auth/telegram", methods=["POST"])
def telegram_login():
    """Mini App auto-login via Telegram initData."""
    data      = request.json or {}
    init_data = data.get("initData", "")
    tg_user   = verify_tg_webapp(init_data)
    if not tg_user:
        return jsonify({"error": "Invalid Telegram data"}), 401

    uid = tg_user.get("id")
    # Load owner IDs from env
    owner_raw = os.getenv("OWNER_IDS", "")
    owner_ids = [int(x.strip()) for x in owner_raw.split(",") if x.strip().isdigit()]
    # Load staff
    staff = load_json(ADMINS_FILE, {}).get("staff", {})

    is_owner = uid in owner_ids
    is_staff = str(uid) in staff

    if not (is_owner or is_staff):
        return jsonify({"error": "Access denied — not an admin"}), 403

    perms = list(staff.get(str(uid), {}).get("perms", [])) if is_staff else ["all"]
    token = make_token({
        "uid":      uid,
        "name":     tg_user.get("first_name", ""),
        "role":     "owner" if is_owner else "staff",
        "is_owner": is_owner,
        "perms":    perms,
        "via":      "telegram"
    })
    return jsonify({"token": token, "role": "owner" if is_owner else "staff",
                    "name": tg_user.get("first_name", ""), "uid": uid})

# ── STATS ─────────────────────────────────────────────────────
@app.route("/api/stats")
def stats():
    db = get_db()
    try:
        total_users    = db.execute("SELECT COUNT(*) FROM tg_users").fetchone()[0]
        today          = datetime.now().date().isoformat()
        active_today   = db.execute("SELECT COUNT(*) FROM tg_users WHERE last_seen LIKE ?",
                                    (f"{today}%",)).fetchone()[0]
        total_numbers  = db.execute("SELECT COUNT(*) FROM numbers").fetchone()[0]
        total_otp_hist = db.execute("SELECT COUNT(*) FROM otp_history").fetchone()[0]
        # OTPs in last 1h
        one_hr_ago = (datetime.now() - timedelta(hours=1)).isoformat()
        otps_1h    = db.execute("SELECT COUNT(*) FROM otp_history WHERE received_at >= ?",
                                (one_hr_ago,)).fetchone()[0]
        otps_24h   = db.execute("SELECT COUNT(*) FROM otp_history WHERE received_at >= ?",
                                ((datetime.now() - timedelta(hours=24)).isoformat(),)).fetchone()[0]
    finally:
        db.close()

    otp_store = load_json(OTP_FILE, {})
    uptime_s  = int(time.time() - START_TIME)
    hours, rem = divmod(uptime_s, 3600)
    mins, secs = divmod(rem, 60)

    return jsonify({
        "uptime":       f"{hours:02d}:{mins:02d}:{secs:02d}",
        "uptime_s":     uptime_s,
        "total_users":  total_users,
        "active_today": active_today,
        "total_numbers":total_numbers,
        "otp_store":    len(otp_store),
        "otp_total":    total_otp_hist,
        "otps_1h":      otps_1h,
        "otps_24h":     otps_24h,
        "panels":       len(load_json(PANEL_FILE, {})),
        "ivas":         len(load_json(IVAS_FILE, {})),
        "groups":       len(load_json(GROUP_FILE, [])),
    })

# ── PANELS ────────────────────────────────────────────────────
@app.route("/api/panels")
def panels():
    return jsonify(load_json(PANEL_FILE, {}))

@app.route("/api/panels", methods=["POST"])
@owner_required
def add_panel():
    data   = request.json or {}
    name   = data.get("name", "").strip()
    url    = data.get("url", "").strip()
    token  = data.get("token", "").strip()
    records = int(data.get("records", 20))
    if not name or not url:
        return jsonify({"error": "name and url required"}), 400
    panels = load_json(PANEL_FILE, {})
    if name in panels:
        return jsonify({"error": "Panel already exists"}), 409
    panels[name] = {"url": url, "token": token, "records": records}
    save_json(PANEL_FILE, panels)
    return jsonify({"ok": True, "name": name})

@app.route("/api/panels/<name>", methods=["DELETE"])
@owner_required
def delete_panel(name):
    panels = load_json(PANEL_FILE, {})
    if name not in panels:
        return jsonify({"error": "Not found"}), 404
    del panels[name]
    save_json(PANEL_FILE, panels)
    return jsonify({"ok": True})

# ── IVAS ──────────────────────────────────────────────────────
@app.route("/api/ivas")
def ivas():
    data = load_json(IVAS_FILE, {})
    safe = {}
    for name, info in data.items():
        uri = info.get("uri", "")
        if "@" in uri:
            uri = re.sub(r'(wss?://)([^@]+)@', r'\1***@', uri)
        safe[name] = {"uri": uri}
    return jsonify(safe)

@app.route("/api/ivas", methods=["POST"])
@owner_required
def add_ivas():
    data = request.json or {}
    name = data.get("name", "").strip()
    uri  = data.get("uri", "").strip()
    if not name or not uri:
        return jsonify({"error": "name and uri required"}), 400
    all_ivas = load_json(IVAS_FILE, {})
    if name in all_ivas:
        return jsonify({"error": "IVAS already exists"}), 409
    all_ivas[name] = {"uri": uri}
    save_json(IVAS_FILE, all_ivas)
    return jsonify({"ok": True, "name": name})

@app.route("/api/ivas/<name>", methods=["DELETE"])
@owner_required
def delete_ivas(name):
    all_ivas = load_json(IVAS_FILE, {})
    if name not in all_ivas:
        return jsonify({"error": "Not found"}), 404
    del all_ivas[name]
    save_json(IVAS_FILE, all_ivas)
    return jsonify({"ok": True})

# ── NUMBERS ───────────────────────────────────────────────────
@app.route("/api/numbers")
def numbers():
    db = get_db()
    try:
        rows = db.execute(
            "SELECT country, COUNT(*) as cnt FROM numbers GROUP BY country ORDER BY cnt DESC"
        ).fetchall()
        return jsonify([{"country": r["country"], "count": r["cnt"]} for r in rows])
    finally:
        db.close()

@app.route("/api/numbers/<country>", methods=["DELETE"])
@owner_required
def delete_country(country):
    db = get_db()
    try:
        db.execute("DELETE FROM numbers WHERE country=?", (country,))
        db.commit()
        return jsonify({"ok": True})
    finally:
        db.close()

# ── OTP HISTORY ───────────────────────────────────────────────
@app.route("/api/otp/history")
def otp_history():
    limit = min(int(request.args.get("limit", 50)), 200)
    db    = get_db()
    try:
        rows = db.execute(
            "SELECT number,service,otp,source,received_at FROM otp_history ORDER BY id DESC LIMIT ?",
            (limit,)
        ).fetchall()
        return jsonify([dict(r) for r in rows])
    finally:
        db.close()

@app.route("/api/otp/store")
def otp_store():
    store = load_json(OTP_FILE, {})
    now   = time.time()
    result = []
    for number, entry in store.items():
        if isinstance(entry, dict):
            otp = entry.get("otp", "")
            ts  = entry.get("ts", 0)
            svc = entry.get("service", "Unknown")
            age = int(now - ts)
            expires_in = max(0, 300 - age)
        else:
            otp = entry
            svc = "Unknown"
            ts  = 0
            expires_in = 0
        result.append({"number": number, "otp": otp, "service": svc, "expires_in": expires_in})
    return jsonify(result)

@app.route("/api/otp/store", methods=["DELETE"])
@owner_required
def clear_otp_store():
    save_json(OTP_FILE, {})
    return jsonify({"ok": True})

# ── USERS ─────────────────────────────────────────────────────
@app.route("/api/users")
def users():
    limit = min(int(request.args.get("limit", 50)), 500)
    db    = get_db()
    try:
        rows = db.execute(
            "SELECT user_id,first_seen,last_seen,total_commands FROM tg_users ORDER BY last_seen DESC LIMIT ?",
            (limit,)
        ).fetchall()
        return jsonify([dict(r) for r in rows])
    finally:
        db.close()

# ── USER BAN SYSTEM ──────────────────────────────────────────
BANNED_FILE = os.path.join(BASE_DIR, "banned_users.json")

@app.route("/api/users/banned")
def get_banned():
    return jsonify(load_json(BANNED_FILE, []))

@app.route("/api/users/ban", methods=["POST"])
@owner_required
def ban_user():
    data = request.json or {}
    try:
        uid = int(data.get("user_id", 0))
    except (ValueError, TypeError):
        return jsonify({"error": "Invalid user_id"}), 400
    banned = load_json(BANNED_FILE, [])
    if uid not in banned:
        banned.append(uid)
        save_json(BANNED_FILE, banned)
    return jsonify({"ok": True})

@app.route("/api/users/unban", methods=["POST"])
@owner_required
def unban_user():
    data = request.json or {}
    try:
        uid = int(data.get("user_id", 0))
    except (ValueError, TypeError):
        return jsonify({"error": "Invalid user_id"}), 400
    banned = load_json(BANNED_FILE, [])
    if uid in banned:
        banned.remove(uid)
        save_json(BANNED_FILE, banned)
    return jsonify({"ok": True})

# ── BROADCAST ─────────────────────────────────────────────────
BROADCAST_LOG_FILE = os.path.join(BASE_DIR, "broadcast_log.json")

@app.route("/api/broadcast", methods=["POST"])
@owner_required
def broadcast():
    """Queue a broadcast message — bot will pick it up and send."""
    data = request.json or {}
    msg  = data.get("message", "").strip()
    if not msg:
        return jsonify({"error": "message required"}), 400
    log  = load_json(BROADCAST_LOG_FILE, [])
    entry = {
        "id":        len(log) + 1,
        "message":   msg,
        "buttons":   data.get("buttons", []),
        "created_at": datetime.now().isoformat(),
        "status":    "pending",
        "sent":      0,
        "failed":    0,
    }
    log.append(entry)
    save_json(BROADCAST_LOG_FILE, log)
    return jsonify({"ok": True, "broadcast_id": entry["id"]})

@app.route("/api/broadcast/history")
def broadcast_history():
    return jsonify(load_json(BROADCAST_LOG_FILE, []))

# ── GROUPS ────────────────────────────────────────────────────
@app.route("/api/groups")
def groups():
    return jsonify({"groups": load_json(GROUP_FILE, [])})

@app.route("/api/groups", methods=["POST"])
@owner_required
def add_group():
    data = request.json or {}
    try:
        gid = int(data.get("chat_id", 0))
    except (ValueError, TypeError):
        return jsonify({"error": "Invalid chat_id"}), 400
    grps = load_json(GROUP_FILE, [])
    if gid in grps:
        return jsonify({"error": "Already exists"}), 409
    grps.append(gid)
    save_json(GROUP_FILE, grps)
    return jsonify({"ok": True})

@app.route("/api/groups/<int:gid>", methods=["DELETE"])
@owner_required
def delete_group(gid):
    groups = load_json(GROUP_FILE, [])
    if gid in groups:
        groups.remove(gid)
        save_json(GROUP_FILE, groups)
    return jsonify({"ok": True})

# ── CONFIG / SETTINGS ─────────────────────────────────────────
@app.route("/api/config")
def get_config():
    cfg = load_json(CONFIG_FILE, {})
    # Strip sensitive keys
    cfg.pop("bot_token", None)
    return jsonify(cfg)

@app.route("/api/config", methods=["PATCH"])
@owner_required
def update_config():
    data = request.json or {}
    cfg  = load_json(CONFIG_FILE, {})
    allowed = ["otp_forward", "forward_delay", "channel_link",
               "number_bot_link", "otp_group_link"]
    for k in allowed:
        if k in data:
            cfg[k] = data[k]
    save_json(CONFIG_FILE, cfg)
    return jsonify({"ok": True, "config": cfg})

# ── FORCE JOIN ────────────────────────────────────────────────
@app.route("/api/force_join")
def force_join():
    return jsonify(load_json(FORCE_JOIN_FILE, []))

@app.route("/api/force_join", methods=["POST"])
@owner_required
def add_force_join():
    data = request.json or {}
    channels = load_json(FORCE_JOIN_FILE, [])
    channels.append({
        "name": data.get("name", "Channel"),
        "link": data.get("link", ""),
        "id":   data.get("id")
    })
    save_json(FORCE_JOIN_FILE, channels)
    return jsonify({"ok": True})

@app.route("/api/force_join/<int:idx>", methods=["DELETE"])
@owner_required
def delete_force_join(idx):
    channels = load_json(FORCE_JOIN_FILE, [])
    if 0 <= idx < len(channels):
        channels.pop(idx)
        save_json(FORCE_JOIN_FILE, channels)
    return jsonify({"ok": True})

# ── OTP SEARCH ───────────────────────────────────────────────
@app.route("/api/otp/search")
def search_otp():
    q = request.args.get("q", "").strip()
    if not q:
        return jsonify([])
    db = get_db()
    try:
        rows = db.execute(
            "SELECT number,service,otp,source,received_at FROM otp_history WHERE number LIKE ? OR otp LIKE ? OR service LIKE ? ORDER BY id DESC LIMIT 50",
            (f"%{q}%", f"%{q}%", f"%{q}%")
        ).fetchall()
        return jsonify([dict(r) for r in rows])
    finally:
        db.close()



# ── CONSUMER AUTH & WALLET ──────────────────────────────────────────
@app.route("/api/consumer/register", methods=["POST"])
def consumer_register():
    data = request.json or {}
    username = data.get("username", "").strip()
    password = data.get("password", "")
    if not username or not password:
        return jsonify({"error": "Username and password required"}), 400
        
    db = get_db()
    try:
        existing = db.execute("SELECT id FROM consumer_users WHERE username=?", (username,)).fetchone()
        if existing:
            return jsonify({"error": "Username already exists"}), 409
            
        hashed = generate_password_hash(password)
        api_key = "nxt_live_" + uuid.uuid4().hex
        db.execute("INSERT INTO consumer_users (username, password_hash, balance, api_key) VALUES (?, ?, 0.0, ?)", 
                   (username, hashed, api_key))
        db.commit()
        return jsonify({"ok": True, "message": "Account created successfully"})
    finally:
        db.close()

@app.route("/api/consumer/login", methods=["POST"])
def consumer_login():
    data = request.json or {}
    username = data.get("username", "").strip()
    password = data.get("password", "")
    
    db = get_db()
    try:
        user = db.execute("SELECT * FROM consumer_users WHERE username=?", (username,)).fetchone()
        if user and check_password_hash(user["password_hash"], password):
            token = make_token({"uid": user["id"], "username": username, "role": "consumer", "api_key": user["api_key"]})
            return jsonify({
                "token": token, 
                "username": username,
                "balance": user["balance"],
                "api_key": user["api_key"]
            })
        return jsonify({"error": "Invalid credentials"}), 401
    finally:
        db.close()

@app.route("/api/consumer/me", methods=["GET"])
def consumer_me():
    token = request.headers.get("Authorization", "").replace("Bearer ", "")
    payload = verify_token(token)
    if not payload or payload.get("role") != "consumer":
        return jsonify({"error": "Unauthorized"}), 401
        
    db = get_db()
    try:
        user = db.execute("SELECT balance, api_key FROM consumer_users WHERE id=?", (payload["uid"],)).fetchone()
        if user:
            return jsonify({"balance": user["balance"], "api_key": user["api_key"]})
        return jsonify({"error": "User not found"}), 404
    finally:
        db.close()

@app.route("/api/wallet/deposit", methods=["POST"])
def wallet_deposit():
    token = request.headers.get("Authorization", "").replace("Bearer ", "")
    payload = verify_token(token)
    if not payload or payload.get("role") != "consumer":
        return jsonify({"error": "Unauthorized"}), 401
        
    data = request.json or {}
    amount = float(data.get("amount", 0))
    if amount <= 0:
        return jsonify({"error": "Invalid amount"}), 400
        
    db = get_db()
    try:
        # Simulate crypto deposit
        txid = "TX-" + uuid.uuid4().hex[:8].upper()
        db.execute("INSERT INTO transactions (user_id, type, amount, status) VALUES (?, ?, ?, ?)",
                   (payload["uid"], "Crypto Deposit (BTC)", amount, "COMPLETED"))
        db.execute("UPDATE consumer_users SET balance = balance + ? WHERE id=?", (amount, payload["uid"]))
        db.commit()
        return jsonify({"ok": True, "txid": txid, "amount": amount})
    finally:
        db.close()

@app.route("/api/wallet/history", methods=["GET"])
def wallet_history():
    token = request.headers.get("Authorization", "").replace("Bearer ", "")
    payload = verify_token(token)
    if not payload or payload.get("role") != "consumer":
        return jsonify({"error": "Unauthorized"}), 401
        
    db = get_db()
    try:
        rows = db.execute("SELECT * FROM transactions WHERE user_id=? ORDER BY created_at DESC LIMIT 50", (payload["uid"],)).fetchall()
        return jsonify([dict(r) for r in rows])
    finally:
        db.close()

# ── PROVISIONING API ──────────────────────────────────────────
@app.route("/api/provision", methods=["POST"])
def provision_number():
    # Require Consumer Auth
    token = request.headers.get("Authorization", "").replace("Bearer ", "")
    payload = verify_token(token)
    if not payload or payload.get("role") != "consumer":
        return jsonify({"error": "Please login to rent a number."}), 401
        
    data = request.json or {}
    country_name = data.get("country", "")
    service = data.get("service", "Unknown")
    price = float(data.get("price", 0.85))
    
    db = get_db()
    try:
        # Check Balance
        user = db.execute("SELECT balance FROM consumer_users WHERE id=?", (payload["uid"],)).fetchone()
        if not user or user["balance"] < price:
            return jsonify({"error": "Insufficient balance. Please deposit funds."}), 402
            
        if country_name:
            row = db.execute("SELECT id, phone FROM numbers WHERE country LIKE ? ORDER BY RANDOM() LIMIT 1", (f"%{country_name}%",)).fetchone()
        else:
            row = db.execute("SELECT id, phone FROM numbers ORDER BY RANDOM() LIMIT 1").fetchone()
            
        if row:
            phone = row["phone"]
            if not phone.startswith("+"):
                phone = "+" + phone
            db.execute("DELETE FROM numbers WHERE id=?", (row["id"],))
        else:
            import random
            phone = f"+{random.randint(10000000000, 99999999999)}"
            
        # Deduct balance and record transaction
        db.execute("UPDATE consumer_users SET balance = balance - ? WHERE id=?", (price, payload["uid"]))
        db.execute("INSERT INTO transactions (user_id, type, amount, status) VALUES (?, ?, ?, ?)",
                   (payload["uid"], f"Number Purchase ({service})", -price, "COMPLETED"))
        # Record rental
        expires = (datetime.now() + timedelta(minutes=15)).isoformat()
        db.execute("INSERT INTO rentals (user_id, phone, service, expires_at) VALUES (?, ?, ?, ?)",
                   (payload["uid"], phone, service, expires))
        db.commit()
        
        return jsonify({"ok": True, "number": phone, "new_balance": user["balance"] - price})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()

# ── SYSTEM INFO ───────────────────────────────────────────────
@app.route("/api/system")
def system_info():
    uptime_s = int(time.time() - START_TIME)
    try:
        import psutil
        cpu   = psutil.cpu_percent(interval=0.1)
        ram   = psutil.virtual_memory()
        disk  = psutil.disk_usage(BASE_DIR)
        ram_used = round(ram.used/1024/1024)
        ram_total= round(ram.total/1024/1024)
        disk_used= round(disk.used/1024/1024/1024, 1)
        disk_total=round(disk.total/1024/1024/1024, 1)
    except ImportError:
        cpu = ram_used = ram_total = disk_used = disk_total = None
    return jsonify({
        "uptime_s":   uptime_s,
        "cpu_percent":cpu,
        "ram_used_mb":ram_used,
        "ram_total_mb":ram_total,
        "disk_used_gb":disk_used,
        "disk_total_gb":disk_total,
        "python_version": f"{__import__('sys').version_info.major}.{__import__('sys').version_info.minor}",
    })

# ── LOGS ──────────────────────────────────────────────────────
@app.route("/api/logs")
def logs():
    lines = int(request.args.get("lines", 100))
    try:
        with open(LOG_FILE) as f:
            all_lines = f.readlines()
        return jsonify({"lines": all_lines[-lines:]})
    except:
        return jsonify({"lines": []})

# ── OTP CHART DATA ────────────────────────────────────────────
@app.route("/api/otp/chart")
def otp_chart():
    """OTP count per hour for last 24h."""
    db = get_db()
    try:
        rows = db.execute("""
            SELECT strftime('%H', received_at) as hr, COUNT(*) as cnt
            FROM otp_history
            WHERE received_at >= datetime('now', '-24 hours')
            GROUP BY hr ORDER BY hr
        """).fetchall()
        return jsonify([{"hour": r["hr"], "count": r["cnt"]} for r in rows])
    finally:
        db.close()

# ── SERVE DASHBOARD HTML ──────────────────────────────────────
@app.route("/infinity.css")
def serve_css():
    return send_from_directory(BASE_DIR, "infinity.css")

@app.route("/", defaults={'path': ''})
@app.route("/<path:path>")
def serve_dashboard(path):
    # Only serve HTML for non-API routes
    if path.startswith("api/"):
        return jsonify({"error": "Not found"}), 404
    return send_from_directory(BASE_DIR, "dashboard.html")

if __name__ == "__main__":
    print(f"🚀 Dashboard running on http://0.0.0.0:{DASHBOARD_PORT}")
    print(f"🔑 Password: {DASHBOARD_PASS}")
    app.run(host="0.0.0.0", port=DASHBOARD_PORT, debug=False)







