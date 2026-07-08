# ╔══════════════════════════════════════════════════════════════╗
# ║     乂 𝐁𝐋𝐀𝐙𝐄 𝐍𝐗𝐓 乂 OTP Bot — Full System Bot                         ║
# ║     Numbers + OTP Forwarding + Full Admin Suite             ║
# ║     Developed by J.A.R.V.I.S.                    ║
# ║     POWERED BY BLAZENXT                   ║
# ╚══════════════════════════════════════════════════════════════╝
# ╔══════════════════════════════════════════════════════════════╗
# ║                        IMPORTS                               ║
# ╚══════════════════════════════════════════════════════════════╝

import asyncio
import requests
import re
import ssl
import json
import os
from dotenv import load_dotenv
load_dotenv()
import sys
import time
import logging
import sqlite3
import websockets
import phonenumbers
from phonenumbers import geocoder
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, List
from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup, Update, CopyTextButton
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler,
    MessageHandler, filters, ContextTypes
)

# ═══════════════════════════════════════════════════════════════
#  CONFIGURATION
# ═══════════════════════════════════════════════════════════════
BOT_TOKEN      = os.getenv("BOT_TOKEN", "")
OWNER_IDS      = [int(x.strip()) for x in os.getenv("OWNER_IDS", "").split(",") if x.strip()]
ADMIN_IDS      = [int(x.strip()) for x in os.getenv("ADMIN_IDS", "").split(",") if x.strip()]
OTP_GROUP_LINK = os.getenv("OTP_GROUP_LINK", "https://t.me/+DfUnv_qgZEFkZWU8")
BOT_NAME       = os.getenv("BOT_NAME", "BlazeNXT OTP Bot")
DEV_CONTACT    = os.getenv("DEV_CONTACT", "@firstoget")
REQUIRED_CHANNELS = []
DEFAULT_PANELS = {
    "BLAZENXT PANEL": {
        "url":      "http://your-panel.com/crapi/time/viewstats",
        "token":    "YOUR_OLD_API_TOKEN_HERE",
        "records":  20,
        "api_type": "old"        # 🔵 Old API (viewstats)
    },
    "PS PANEL": {
        "url":      "https://pscall.net/restapi/smsreport",
        "token":    "YOUR_PS_API_TOKEN_HERE",
        "records":  20,
        "api_type": "ps"       # 🟢 PS API (pscall.net)
    },
}
OTP_GROUP_IDS = [int(x.strip()) for x in os.getenv("OTP_GROUP_IDS", "-1003902733109").split(",") if x.strip()]

OTP_FILE      = "otp_store.json"
PANEL_FILE    = "panels.json"
IVAS_FILE     = "ivas.json"
USER_FILE     = "users.json"
GROUP_FILE    = "groups.json"
CONFIG_FILE   = "bot_config.json"
ADMINS_FILE   = "admins.json"
LOG_FILE      = "bot.log"
DB_FILE       = "bot_data.db"

# ═══════════════════════════════════════════════════════════════
#  CUSTOM EMOJI DICTIONARIES (Telegram Premium Custom Emojis)
#  All old emojis removed - replaced with custom emoji IDs
# ═══════════════════════════════════════════════════════════════
COUNTRY_EMOJI_ID = {
    "UA": "5222250679371839695", "UA_2": "5280587278828193324",
    "US": "5224321781321442532", "PL": "5224670399521892983",
    "KZ": "5222276376161171525", "AZ": "5224426544163728284",
    "EU": "5222108911091331711", "UN": "5451772687993031127",
    "AM": "5224369957969603463", "RU": "5280582975270963511",
    "CN": "5224435456220868088", "UZ": "5222404546575219535",
    "DE": "5222165617544542414", "JP": "5222390089715299207",
    "TR": "5224601903383457698", "BY": "5280820319458707404",
    "BY_2": "5222398507851199882", "GB": "5224518800061245598",
    "IN": "5222300011366200403", "BR": "5224688610183228070",
    "ZM": "5224646626877911277", "YE": "5222300655611294950",
    "VI": "5224395882392201810", "VN": "5222359651282071925",
    "VA": "5222420266155520507", "VU": "5222126748090512778",
    "UY": "5222466849370813232", "AE": "5224565851427976312",
    "US_2": "5222253007244113340", "UG": "5222464040462200940",
    "TM": "5224256935905208951", "TN": "5221991375016310330",
    "TT": "5224391883777651050", "TG": "5222408051268532030",
    "TH": "5224638530864556281", "TZ": "5224397364155923150",
    "TJ": "5222217865821696536", "CH": "5224707263226194753",
    "SE": "5222201098269373561", "SZ": "5224269666188274723",
    "SR": "5224567367551428669", "SD": "5224372990216514135",
    "ES": "5222024776976970940", "LK": "5224277294050192388",
    "SS": "5224618146949773268", "KR": "5222345550904439270",
    "ZA": "5224696216570309138", "SO": "5222370504664428325",
    "SI": "5224660718665607511", "SK": "5222401879400528047",
    "SG": "5224194023224257181", "SL": "5224420995065983217",
    "SC": "5224467496676896871", "RS": "5222145396838512729",
    "SN": "5224358988623130949", "SA": "5224698145010624573",
    "ST": "5221953304426198315", "WS": "5224660353593387686",
    "VC": "5224541228380467535", "LC": "5222000927023577045",
    "PS": "5222041677673282461", "PS_2": "5222370620628546719",
    "RW": "5222449197055227754", "RO": "5222273794885826118",
    "QA": "5222225596762830469", "PR": "5224220115150582423",
    "PT": "5224404094369672274", "PH": "5222065042295376892",
    "PE": "5224482026551258766", "PY": "5222152565138929235",
    "PG": "5224500164198149905", "PA": "5222111719999945107",
    "PK": "5224637061985742245", "OM": "5222396686785066306",
    "NO": "5224465228934163949", "NG": "5224723614166691638",
    "NE": "5222099049846420864", "NZ": "5224573595254009705",
    "NL": "5224516489368841614", "NP": "5222444378101925267",
    "NA": "5224690826386351746", "MZ": "5222470388423864826",
    "MA": "5224530035695693965", "ME": "5224463399278096980",
    "MN": "5224192257992701543", "MC": "5221937224068640464",
    "MD": "5224216473018314447", "FM": "5222280486444873367",
    "MX": "5221971386238514431", "MU": "5224238347286752315",
    "MH": "5224538449536624503", "MY": "5224312886444174057",
    "KE": "5222089648163009103", "KE_2": "5222279743415531561",
    "MG": "5222042605386217334", "MK": "5222470435668505656",
    "LU": "5224499567197700690", "LT": "5224245902134226386",
    "LY": "5222194286451242896", "LR": "5221998371518034740",
    "LS": "5224245850594619415", "LB": "5222244425899455269",
    "LV": "5224401229626484931", "LA": "5224200843632324642",
    "KG": "5224388147156102493", "KW": "5221949726718442491",
    "XK": "5222197129719592160", "KI": "5224652244695134610",
    "JO": "5222292177345853436", "JM": "5222007034467074185",
    "IE": "5224257017509588818", "IE_2": "5222233374948602940",
    "IT": "5222460101977190141", "IL": "5224720599099648709",
    "IQ": "5221980268230882832", "IR": "5224374154152653367",
    "ID": "5224405893960969756", "IS": "5222063229819172521",
    "HU": "5224691998912427164", "HN": "5222229234600130045",
    "HN_2": "5222434624231191289", "HT": "5224683146984831315",
    "GY": "5224570532942329532", "GW": "5224705704153066489",
    "GN": "5222337588035073000", "GT": "5222128302868672826",
    "GD": "5222234560359577687", "GR": "5222463490706389920",
    "GH": "5224511339703056124", "GE": "5222152195771742239",
    "GM": "5221949872747330159", "GA": "5224669733801963467",
    "FR": "5222029789203804982", "FI": "5224282903277482188",
    "FJ": "5221962676044838178", "ET": "5224467805914542024",
    "EE": "5222195463272281351", "GQ": "5222172811614762423",
    "SV": "5224337131534559907", "EG": "5222161185138292290",
    "EC": "5224191188545840926", "TL": "5224515905253291409",
    "DO": "5224286412265763450", "DM": "5222337489250824921",
    "DJ": "5224203012590810589", "DK": "5222297215342490217",
    "CY": "5222431454545327055", "HR": "5221967765581085099",
    "CR": "5222453801260168022", "CG": "5222104268231684600",
    "CD": "5224398158724871677", "KM": "5222398735484466247",
    "CO": "5224455152940886669", "CL": "5222350726340032308",
    "CZ": "5222073533445714675", "TD": "5222060468155204001",
    "CF": "5222073662294733523", "CV": "5222347737042792258",
    "CA": "5222001124592071204", "CM": "5222270788408717651",
    "KH": "5224189882875785448", "BI": "5224490444687158452",
    "BF": "5222356541725749790", "BG": "5222092074819530668",
    "BN": "5224435958732042406", "BW": "5224288456670196085",
    "BA": "5224496092569155254", "BO": "5224675484763170798",
    "BT": "5224541065171710147", "BJ": "5222024115552009151",
    "BZ": "5224316292353241916", "BE": "5224513182244024630",
    "BB": "5222156533688712094", "BD": "5224407289825340729",
    "BH": "5224492892818518587", "BS": "5224504167107668172",
    "AT": "5224520754271366661", "AU": "5224659803837574114",
    "AR": "5221980461504411710", "AG": "5224544866217765554",
    "AO": "5224379767674907895", "AD": "5221987861733061751",
    "DZ": "5224260376174015500", "AL": "5224312057515486246",
    "AF": "5222096009009575868", "ZW": "5222060442385397848",
    "VE": "5294476442854247878", "FO": "5280985770188885026",
    "MQ": "5281027792148909351",
    "DEFAULT": "5222250679371839695",
}

APP_EMOJI_ID = {
    "whatsapp":  "5334998226636390258",
    "telegram":  "5330237710655306682",
    "instagram": "5319160079465857105",
    "facebook":  "5323261730283863478",
    "google":    "5359758030198031389",
    "gmail":     "5359758030198031389",
    "twitter":   "5330337435500951363",
    "tiktok":    "5327982530702359565",
    "snapchat":  "5330248916224983855",
    "binance":   "5359437015752401733",
    "bybit":     "5359437015752401733",
    "discord":   "5373026167722876724",
    "netflix":   "5373026167722876724",
    "amazon":    "5373026167722876724",
    "paypal":    "5373026167722876724",
    "spotify":   "5373026167722876724",
    "DEFAULT":   "5373026167722876724",
}

SERVICE_HASHTAGS = {
    "whatsapp": "WS", "telegram": "TG", "instagram": "IG", "facebook": "FB",
    "google": "GG", "gmail": "GG", "twitter": "TW", "tiktok": "TT",
    "snapchat": "SC", "netflix": "NF", "amazon": "AM", "paypal": "PP",
    "binance": "BN", "bybit": "BB", "discord": "DC", "microsoft": "MS",
    "yahoo": "YH", "apple": "AP", "spotify": "SP", "vk": "VK", "line": "LN",
    "wechat": "WC", "viber": "VB", "imo": "IM", "kakaotalk": "KT",
    "truecaller": "TC", "linkedin": "LI", "shopee": "SH", "lazada": "LZ",
    "gojek": "GJ", "grab": "GR", "foodpanda": "FP", "deliveroo": "DR",
    "uber": "UB", "bolt": "BL", "indriver": "IDR", "careem": "CR",
    "tinder": "TN", "bumble": "BM", "okcupid": "OK", "hinge": "HG",
    "gochat": "GH",
}

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    handlers=[logging.FileHandler(LOG_FILE), logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

STATS = {"start_time": time.time(), "otps_sent": 0, "otps_dropped": 0,
         "errors": 0, "panel_hits": {}, "ivas_hits": {}}

# ── OTP Send Queue ─────────────────────────────────────────────
OTP_QUEUE: asyncio.Queue = asyncio.Queue()

PANEL_ADD_STATES = {}
IVAS_ADD_STATES  = {}
BROADCAST_STATES = {}
SETTING_STATES   = {}
NB_STATE         = {}
FETCH_STATES     = {}
STATE_TIMEOUT    = 300

IVAS_TASKS: Dict[str, asyncio.Task] = {}
REST_TASKS: Dict[str, asyncio.Task] = {}

OTP_LOG: List[dict] = []
OTP_LOG_MAX = 200

# ═══════════════════════════════════════════════════════════════
#  SQLITE DATABASE
# ═══════════════════════════════════════════════════════════════
def init_db():
    conn = sqlite3.connect(DB_FILE, check_same_thread=False, timeout=15)
    conn.execute('PRAGMA journal_mode=WAL;')
    conn.execute('PRAGMA synchronous=NORMAL;')
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS numbers
                 (id INTEGER PRIMARY KEY, country TEXT, phone TEXT,
                  added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)""")
    c.execute("""CREATE TABLE IF NOT EXISTS tg_users
                 (user_id INTEGER PRIMARY KEY, first_seen TEXT,
                  last_seen TEXT, total_commands INTEGER DEFAULT 0)""")
    c.execute("""CREATE TABLE IF NOT EXISTS consumer_users
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                  username TEXT UNIQUE, password_hash TEXT, 
                  balance REAL DEFAULT 0.0, api_key TEXT)""")
    c.execute("""CREATE TABLE IF NOT EXISTS rentals
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                  user_id INTEGER, phone TEXT, service TEXT, 
                  status TEXT DEFAULT 'active', expires_at TIMESTAMP)""")
    c.execute("""CREATE TABLE IF NOT EXISTS transactions
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                  user_id INTEGER, type TEXT, amount REAL, 
                  status TEXT, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)""")
    c.execute("""CREATE TABLE IF NOT EXISTS otp_history
                 (id INTEGER PRIMARY KEY, number TEXT, service TEXT,
                  otp TEXT, source TEXT,
                  received_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)""")
    c.execute("""CREATE TABLE IF NOT EXISTS assigned_numbers
                 (phone TEXT PRIMARY KEY, user_id INTEGER NOT NULL,
                  assigned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)""")
    conn.commit()
    return conn

db = init_db()

def db_add_user(user_id: int):
    c = db.cursor()
    now = datetime.now().isoformat()
    c.execute("INSERT OR IGNORE INTO tg_users (user_id,first_seen,last_seen) VALUES (?,?,?)",
              (user_id, now, now))
    c.execute("UPDATE tg_users SET last_seen=?,total_commands=total_commands+1 WHERE user_id=?",
              (now, user_id))
    db.commit()

def db_get_countries():
    c = db.cursor()
    c.execute("SELECT country,COUNT(*) FROM numbers GROUP BY country ORDER BY COUNT(*) DESC")
    return c.fetchall()

def db_get_country_numbers(country: str, limit: int = 9999):
    c = db.cursor()
    c.execute("SELECT phone FROM numbers WHERE country=? LIMIT ?", (country, limit))
    return [r[0] for r in c.fetchall()]

def db_pop_number(country: str):
    c = db.cursor()
    c.execute("SELECT id,phone FROM numbers WHERE country=? LIMIT 1", (country,))
    row = c.fetchone()
    if row:
        c.execute("DELETE FROM numbers WHERE id=?", (row[0],))
        db.commit()
        return row[1]
    return None

def db_pop_numbers(country: str, count: int = 3):
    c = db.cursor()
    c.execute("SELECT id,phone FROM numbers WHERE country=? LIMIT ?", (country, count))
    rows = c.fetchall()
    if rows:
        ids = [r[0] for r in rows]
        c.execute(f"DELETE FROM numbers WHERE id IN ({','.join('?'*len(ids))})", ids)
        db.commit()
        return [r[1] for r in rows]
    return []

def db_delete_country(country: str):
    c = db.cursor()
    c.execute("DELETE FROM numbers WHERE country=?", (country,))
    db.commit()

def db_add_numbers(country: str, nums: list):
    c = db.cursor()
    c.executemany("INSERT INTO numbers (country,phone) VALUES (?,?)",
                  [(country, n) for n in nums])
    db.commit()

def db_total_numbers():
    c = db.cursor()
    c.execute("SELECT COUNT(*) FROM numbers")
    return c.fetchone()[0]

def db_save_otp_history(number: str, service: str, otp: str, source: str):
    c = db.cursor()
    c.execute("INSERT INTO otp_history (number,service,otp,source) VALUES (?,?,?,?)",
              (number, service, otp or "N/A", source))
    db.commit()

def db_assign_numbers(user_id: int, phones: list):
    c = db.cursor()
    for phone in phones:
        clean = re.sub(r"[^0-9]", "", phone)
        c.execute("INSERT OR REPLACE INTO assigned_numbers (phone, user_id) VALUES (?,?)",
                  (clean, user_id))
    db.commit()

def db_get_owner_of_number(number: str) -> Optional[int]:
    clean = re.sub(r"[^0-9]", "", number)
    c = db.cursor()
    c.execute("SELECT user_id FROM assigned_numbers WHERE phone=?", (clean,))
    row = c.fetchone()
    if row:
        return row[0]
    if len(clean) >= 5:
        suffix = clean[-5:]
        c.execute("SELECT user_id FROM assigned_numbers WHERE phone LIKE ?", (f"%{suffix}",))
        row = c.fetchone()
        if row:
            return row[0]
    return None

def db_clear_old_assignments(days: int = 2):
    c = db.cursor()
    c.execute("DELETE FROM assigned_numbers WHERE assigned_at < datetime('now', ?)",
              (f"-{days} days",))
    db.commit()

def db_get_otp_history(limit: int = 20):
    c = db.cursor()
    c.execute("""SELECT number,service,otp,source,received_at FROM otp_history
                 ORDER BY id DESC LIMIT ?""", (limit,))
    return c.fetchall()

def db_search_otp_by_number(target: str):
    c = db.cursor()
    c.execute("""SELECT number,service,otp,source,received_at FROM otp_history
                 WHERE number LIKE ? ORDER BY id DESC LIMIT 10""", (f"%{target}%",))
    return c.fetchall()

def db_clear_otp_history():
    c = db.cursor()
    c.execute("DELETE FROM otp_history")
    db.commit()

def db_user_stats():
    c = db.cursor()
    today    = datetime.now().date().isoformat()
    week_ago = (datetime.now() - timedelta(days=7)).isoformat()
    c.execute("SELECT COUNT(*) FROM tg_users")
    total = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM tg_users WHERE last_seen LIKE ?", (f"{today}%",))
    active_today = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM tg_users WHERE last_seen >= ?", (week_ago,))
    active_week = c.fetchone()[0]
    return total, active_today, active_week

# ═══════════════════════════════════════════════════════════════
#  JSON HELPERS
# ═══════════════════════════════════════════════════════════════
def load_json(file: str, default: Any = None) -> Any:
    if default is None:
        default = {}
    if not os.path.exists(file):
        return default
    try:
        with open(file, 'r') as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Error loading {file}: {e}")
        return default

def save_json(file: str, data: Any) -> None:
    try:
        with open(file, 'w') as f:
            json.dump(data, f, indent=4)
    except Exception as e:
        logger.error(f"Error saving {file}: {e}")

def load_panels():      return load_json(PANEL_FILE, DEFAULT_PANELS.copy())
def save_panels(d):     save_json(PANEL_FILE, d)
def load_ivas():        return load_json(IVAS_FILE, {})
def save_ivas(d):       save_json(IVAS_FILE, d)
def load_otp_store():   return load_json(OTP_FILE, {})
def save_otp_store(d):  save_json(OTP_FILE, d)
def load_users():       return load_json(USER_FILE, {})
def save_users(d):      save_json(USER_FILE, d)
def load_groups():      return load_json(GROUP_FILE, OTP_GROUP_IDS.copy())
def save_groups(d):     save_json(GROUP_FILE, d)

# ═══════════════════════════════════════════════════════════════
#  PERMISSION SYSTEM
# ═══════════════════════════════════════════════════════════════

ALL_PERMISSIONS = {
    "numbers":    "📦 Add/Delete Numbers",
    "panels":     "📡 Manage Panels",
    "ivas":       "🔌 Manage IVAS",
    "groups":     "👥 Manage Groups",
    "broadcast":  "📢 Broadcast",
    "otp_history":"📋 OTP History",
    "fetch_sms":  "🔄 Fetch SMS",
    "files":      "📂 File Manager",
    "settings":   "⚙️ Settings",
    "advanced":   "🔧 Advanced Tools",
    "stats":      "📊 Stats/Status",
}

def load_staff() -> dict:
    data = load_json(ADMINS_FILE, {"owners": list(OWNER_IDS), "staff": {}})
    return data.get("staff", {})

def save_staff(staff: dict):
    data = load_json(ADMINS_FILE, {"owners": list(OWNER_IDS), "staff": {}})
    data["staff"] = staff
    save_json(ADMINS_FILE, data)

def load_admins() -> list:
    staff = load_staff()
    return [int(k) for k in staff.keys()] + list(OWNER_IDS)

def get_staff_perms(uid: int) -> list:
    if is_owner(uid):
        return list(ALL_PERMISSIONS.keys())
    staff = load_staff()
    return staff.get(str(uid), {}).get("perms", [])

def has_perm(uid: int, perm: str) -> bool:
    if is_owner(uid):
        return True
    return perm in get_staff_perms(uid)

def add_staff(uid: int, name: str, perms: list):
    staff = load_staff()
    staff[str(uid)] = {"name": name, "perms": perms}
    save_staff(staff)

def remove_staff(uid: int):
    staff = load_staff()
    staff.pop(str(uid), None)
    save_staff(staff)

def update_staff_perms(uid: int, perms: list):
    staff = load_staff()
    if str(uid) in staff:
        staff[str(uid)]["perms"] = perms
        save_staff(staff)

def load_config():
    return load_json(CONFIG_FILE, {
        "channel_link":    OTP_GROUP_LINK,
        "number_bot_link": "http://t.me/BlazeNXTBot",
        "otp_forward":     True,
        "forward_delay":   0,
        "log_group":       None,
    })

def save_config(c): save_json(CONFIG_FILE, c)

def is_owner(uid: int) -> bool:
    return uid in OWNER_IDS

def is_admin(uid: int) -> bool:
    if is_owner(uid):
        return True
    staff = load_staff()
    return str(uid) in staff

def get_role_label(uid: int) -> str:
    if is_owner(uid):
        return "👑 Owner"
    staff = load_staff()
    entry = staff.get(str(uid))
    if entry:
        perms = entry.get("perms", [])
        return f"🛡️ Staff ({len(perms)} perms)"
    return "👤 User"

API_PANELS = load_panels()

# ═══════════════════════════════════════════════════════════════
#  OTP HELPERS WITH CUSTOM EMOJIS (NO OLD EMOJIS)
# ═══════════════════════════════════════════════════════════════

REGION_LANGUAGE = {
    "DE":"German","AT":"German","CH":"German","FR":"French","BE":"French",
    "ES":"Spanish","MX":"Spanish","AR":"Spanish","PT":"Portuguese","BR":"Portuguese",
    "RU":"Russian","UA":"Russian","BY":"Russian","TR":"Turkish",
    "SA":"Arabic","AE":"Arabic","EG":"Arabic","CN":"Chinese","TW":"Chinese",
    "JP":"Japanese","KR":"Korean","IN":"Hindi","PK":"Urdu","IT":"Italian",
    "NL":"Dutch","PL":"Polish","SE":"Swedish","NO":"Norwegian","DK":"Danish",
    "FI":"Finnish","GR":"Greek","IR":"Persian","TH":"Thai","VN":"Vietnamese",
    "ID":"Indonesian","NG":"English","PH":"Filipino",
}

def get_service_short(service: str) -> str:
    """Get service hashtag using SERVICE_HASHTAGS dictionary"""
    s = service.lower().strip()
    for key, tag in SERVICE_HASHTAGS.items():
        if key in s:
            return tag
    clean = re.sub(r"[^a-zA-Z]", "", service)
    return clean[:2].upper() if clean else "OT"

def get_custom_country_emoji(region_code: str) -> str:
    """
    Get custom emoji ID for country using Telegram custom emoji feature.
    Returns custom emoji HTML tag - NO OLD EMOJIS
    """
    if not region_code:
        return f"<tg-emoji emoji-id=\"{COUNTRY_EMOJI_ID['DEFAULT']}\">🌍</tg-emoji>"
    
    # Try exact match
    if region_code in COUNTRY_EMOJI_ID:
        return f"<tg-emoji emoji-id=\"{COUNTRY_EMOJI_ID[region_code]}\">🌍</tg-emoji>"
    
    # Try with _2 suffix for alternative versions
    if f"{region_code}_2" in COUNTRY_EMOJI_ID:
        return f"<tg-emoji emoji-id=\"{COUNTRY_EMOJI_ID[f'{region_code}_2']}\">🌍</tg-emoji>"
    
    # Try uppercase
    if region_code.upper() in COUNTRY_EMOJI_ID:
        return f"<tg-emoji emoji-id=\"{COUNTRY_EMOJI_ID[region_code.upper()]}\">🌍</tg-emoji>"
    
    # Fallback to DEFAULT
    return f"<tg-emoji emoji-id=\"{COUNTRY_EMOJI_ID['DEFAULT']}\">🌍</tg-emoji>"

def get_app_emoji(service: str) -> str:
    """
    Get custom emoji ID for app/service using Telegram custom emoji feature.
    Returns custom emoji HTML tag - NO OLD EMOJIS
    """
    s = service.lower().strip()
    for key, emoji_id in APP_EMOJI_ID.items():
        if key in s:
            return f"<tg-emoji emoji-id=\"{emoji_id}\">📱</tg-emoji>"
    return f"<tg-emoji emoji-id=\"{APP_EMOJI_ID['DEFAULT']}\">📱</tg-emoji>"

def extract_otp(message: str) -> Optional[str]:
    """
    Extract OTP from SMS text.
    """
    # Split OTP: 3–4 digits, dash or space, 3–4 digits
    m = re.search(r'(?<!\d)(\d{3,4})[\- ](\d{3,4})(?!\d)', message)
    if m:
        combined = m.group(1) + m.group(2)
        if 6 <= len(combined) <= 8:
            return combined

    # Straight 4–6 digit OTP
    for pat in [r'(?<!\d)\d{6}(?!\d)',
                r'(?<!\d)\d{5}(?!\d)',
                r'(?<!\d)\d{4}(?!\d)']:
        m = re.search(pat, message)
        if m:
            return m.group(0)

    return None

def get_country_info(number_str: str) -> tuple:
    """Returns country name and region code (no flag emoji - using custom emojis now)"""
    try:
        if not number_str.startswith("+"):
            number_str = "+" + number_str
        parsed  = phonenumbers.parse(number_str)
        country = geocoder.description_for_number(parsed, "en")
        region  = phonenumbers.region_code_for_number(parsed)
        return country or "Unknown", region or ""
    except:
        return "Unknown", ""

def get_region_code(number_str: str) -> str:
    try:
        n = number_str if number_str.startswith("+") else "+" + number_str
        return phonenumbers.region_code_for_number(phonenumbers.parse(n)) or ""
    except:
        return ""

def get_country_code_str(number_str: str) -> str:
    try:
        n = number_str if number_str.startswith("+") else "+" + number_str
        return f"+{phonenumbers.parse(n).country_code}"
    except:
        return ""

def get_last5(number_str: str) -> str:
    digits = re.sub(r"[^0-9]", "", number_str)
    return digits[-5:] if len(digits) >= 5 else digits

def detect_language_from_text(text: str) -> str:
    """Detect language from SMS message content."""
    if not text:
        return None
    if re.search(r'[\u3041-\u3096\u30A1-\u30FA]', text): return "Japanese"
    if re.search(r'[\uAC00-\uD7AF]', text):               return "Korean"
    if re.search(r'[\u4e00-\u9fff\u3400-\u4DBF]', text):  return "Chinese"
    if re.search(r'[\u0600-\u06FF]', text):                return "Arabic"
    if re.search(r'[\u0400-\u04FF]', text):                return "Russian"
    if re.search(r'[\u0900-\u097F]', text):                return "Hindi"
    if re.search(r'[\u0E00-\u0E7F]', text):                return "Thai"
    if re.search(r'[\u0370-\u03FF]', text):                return "Greek"
    if re.search(r'[\u06A9\u06AF\u06CC\u06BE]', text):    return "Persian"
    if re.search(r'[\u0590-\u05FF]', text):                return "Hebrew"
    return None

def format_number_pkotp(number: str) -> str:
    """
    Format full number as: 4915511-BLAZENXT-03543
    First 7 digits + -BLAZENXT- + last 5 digits
    """
    digits = re.sub(r"[^0-9]", "", number)
    if len(digits) >= 12:
        return f"{digits[:7]}-BLAZENXT-{digits[-5:]}"
    elif len(digits) >= 7:
        mid = len(digits) - 5
        return f"{digits[:mid]}-BLAZENXT-{digits[-5:]}"
    return digits

def format_otp_message(number: str, service: str, otp: str,
                        source_label: str = "", sms_text: str = "") -> str:
    """
    Format OTP message with CUSTOM EMOJIS ONLY - no old flag emojis
    Layout: [CountryEmoji] ┃ [ServiceEmoji] #REGION #SVC
            [number in BLAZENXT format]
            #Language
    """
    region    = get_region_code(number)
    svc       = get_service_short(service)

    # Get custom emojis (NO OLD FLAG EMOJIS)
    country_custom_emoji = get_custom_country_emoji(region)
    app_custom_emoji     = get_app_emoji(service)

    # Number formatted as: 9230267 BLAZENXT 55035
    pkotp_number = format_number_pkotp(number)

    # Detect language from full SMS text first, fallback to region map
    lang = detect_language_from_text(sms_text)
    if not lang:
        lang = REGION_LANGUAGE.get(region, "English")

    # Layout:
    # [CountryEmoji] ┃ [ServiceEmoji]  #WS
    # `9230267 BLAZENXT 55035`
    # #Urdu
    gh_tag = "  <b>#GH</b>" if "gochat" in service.lower() else ""
    return f"{country_custom_emoji} ┃ {app_custom_emoji}  <b>#{region}</b>  <b>{pkotp_number}</b>  <b>#{lang}</b>{gh_tag}"

def get_otp_keyboard(number: str, otp: str) -> InlineKeyboardMarkup:
    TAP_EMOJI   = "5368324170671202286"
    PHONE_EMOJI = "5334956902598927432"
    CHAT_EMOJI  = "5334778871262052427"

    if otp:
        clean_otp = re.sub(r"[^0-9]", "", otp)
        otp_btn = InlineKeyboardButton(
            " • • • • • • • • • •",
            copy_text=CopyTextButton(text=clean_otp),
            api_kwargs={
                "style": "success",
                "icon_custom_emoji_id": TAP_EMOJI
            }
        )
    else:
        otp_btn = InlineKeyboardButton("No OTP Detected", callback_data="no_otp")

    return InlineKeyboardMarkup([
        [otp_btn],
        [
            InlineKeyboardButton(
                " Numbers",
                url="https://t.me/blazenxt_numbers",
                api_kwargs={
                    "style": "danger",
                    "icon_custom_emoji_id": PHONE_EMOJI
                }
            ),
            InlineKeyboardButton(
                " WhatsApp",
                url="https://chat.whatsapp.com/HVqCQ6wX0sz9sqox5QEgrg?mode=hqctcla",
                api_kwargs={
                    "style": "primary",
                    "icon_custom_emoji_id": CHAT_EMOJI
                }
            ),
        ]
    ])

# Shared persistent Bot instance
_shared_bot: Optional[Bot] = None

def get_shared_bot() -> Bot:
    global _shared_bot
    if _shared_bot is None:
        _shared_bot = Bot(token=BOT_TOKEN)
    return _shared_bot

# In-memory caches
_CONFIG_CACHE: dict = {}
_CONFIG_CACHE_TS: float = 0.0
_GROUPS_CACHE: list = []
_GROUPS_CACHE_TS: float = 0.0
_CACHE_TTL: float = 5.0

def get_cached_config() -> dict:
    global _CONFIG_CACHE, _CONFIG_CACHE_TS
    if time.time() - _CONFIG_CACHE_TS > _CACHE_TTL:
        _CONFIG_CACHE = load_config()
        _CONFIG_CACHE_TS = time.time()
    return _CONFIG_CACHE

def get_cached_groups() -> list:
    global _GROUPS_CACHE, _GROUPS_CACHE_TS
    if time.time() - _GROUPS_CACHE_TS > _CACHE_TTL:
        _GROUPS_CACHE = load_groups()
        _GROUPS_CACHE_TS = time.time()
    return _GROUPS_CACHE

async def send_to_all_groups(msg: str, reply_markup=None):
    """Enqueue OTP"""
    config = get_cached_config()
    if not config.get("otp_forward", True):
        STATS["otps_dropped"] += 1
        return
    await OTP_QUEUE.put((msg, reply_markup))

async def _otp_sender_task():
    """Dedicated queue-draining task"""
    bot = get_shared_bot()
    logger.info("📤 OTP sender task started.")
    while True:
        try:
            msg, reply_markup = await OTP_QUEUE.get()
            groups = get_cached_groups()
            if not groups:
                OTP_QUEUE.task_done()
                continue

            async def _send_one(gid):
                for attempt in range(3):
                    try:
                        await bot.send_message(
                            chat_id=gid, text=msg,
                            parse_mode="HTML", reply_markup=reply_markup)
                        STATS["otps_sent"] += 1
                        logger.info(f"✅ OTP sent to group {gid}")
                        return
                    except Exception as e:
                        err = str(e)
                        if "RetryAfter" in err or "Too Many Requests" in err:
                            m = re.search(r"retry after (\d+)", err, re.I)
                            wait = int(m.group(1)) if m else 5
                            logger.warning(f"Flood wait {wait}s for group {gid}")
                            await asyncio.sleep(wait)
                        else:
                            STATS["errors"] += 1
                            logger.error(f"Send failed {gid} attempt {attempt+1}: {e}")
                            if attempt < 2:
                                await asyncio.sleep(1)
                            else:
                                break

            await asyncio.gather(*[_send_one(gid) for gid in groups])
            OTP_QUEUE.task_done()
        except asyncio.CancelledError:
            break
        except Exception as e:
            logger.error(f"_otp_sender_task error: {e}")

async def send_otp_to_owner(number: str, service: str, otp: str,
                             sms_text: str = "", source_label: str = ""):
    """Send OTP privately to the user who was assigned this number"""
    owner_id = db_get_owner_of_number(number)
    if not owner_id:
        return

    clean_otp = re.sub(r"[^0-9]", "", otp) if otp and otp != "N/A" else (otp or "N/A")
    region    = get_region_code(number)
    svc       = get_service_short(service)
    lang      = detect_language_from_text(sms_text) or REGION_LANGUAGE.get(region, "English")

    # Get custom emojis
    country_custom_emoji = get_custom_country_emoji(region)
    app_custom_emoji     = get_app_emoji(service)

    # Number in PKOTP format
    pkotp_number = format_number_pkotp(number)

    msg = f"{country_custom_emoji} ┃ {app_custom_emoji}  <b>#{region}</b>  <b>{pkotp_number}</b>  <b>#{lang}</b>"

    if clean_otp and clean_otp != "N/A":
        otp_btn = InlineKeyboardButton(
            " • • • • • • • • • •",
            copy_text=CopyTextButton(text=clean_otp),
            api_kwargs={
                "style": "success",
                "icon_custom_emoji_id": "5368324170671202286"
            }
        )
    else:
        otp_btn = InlineKeyboardButton("No OTP Detected", callback_data="no_otp")

    kb = InlineKeyboardMarkup([
        [otp_btn],
        [
            InlineKeyboardButton(
                " Numbers",
                url="https://t.me/blazenxt_numbers",
                api_kwargs={
                    "style": "danger",
                    "icon_custom_emoji_id": "5334956902598927432"
                }
            ),
            InlineKeyboardButton(
                " WhatsApp",
                url="https://chat.whatsapp.com/HVqCQ6wX0sz9sqox5QEgrg?mode=hqctcla",
                api_kwargs={
                    "style": "primary",
                    "icon_custom_emoji_id": "5334778871262052427"
                }
            ),
        ]
    ])
    bot = get_shared_bot()
    try:
        await bot.send_message(chat_id=owner_id, text=msg,
                               parse_mode="HTML", reply_markup=kb)
        logger.info(f"✅ OTP DM sent to user {owner_id} for ...{number[-5:]}")
    except Exception as e:
        logger.warning(f"Could not DM user {owner_id}: {e}")

def log_otp_memory(number: str, service: str, otp: str, source: str):
    global OTP_LOG
    OTP_LOG.append({"number": number, "service": service, "otp": otp or "N/A",
                    "source": source, "time": datetime.now().strftime("%H:%M:%S")})
    if len(OTP_LOG) > OTP_LOG_MAX:
        OTP_LOG = OTP_LOG[-OTP_LOG_MAX:]
    db_save_otp_history(number, service, otp, source)

# ═══════════════════════════════════════════════════════════════
#  REST PANEL FETCH  ── Universal Auto-Detect Engine
#
#  Supported API types (auto-detected, no manual selection needed):
#
#  [1] OLD API  (original viewstats panels)
#      Fields: dt / num / cli / message
#      Auth:   ?token=TOKEN&records=N
#      Detect: response has "status":"success" + "data" list
#              with keys "dt","num","cli","message"
#
#  [2] MO API   (MOAPI-Purple / reseller/mdr.php)
#      URL:    http://137.74.1.203/crapi/reseller/mdr.php
#      Fields: datetime / number / cli / message
#      Auth:   ?token=TOKEN&fromdate=...&todate=...&records=N
#      Detect: response has "status":"Success" + "data" list
#              with keys "datetime","number","cli","message"
#
#  [3] PS API   (pscall.net/restapi/smsreport)
#      URL:    https://pscall.net/restapi/smsreport
#      Fields: dateadded / num / cli / sms
#      Auth:   ?key=KEY  (uses "key" not "token")
#      Detect: response is a list of objects with "num","sms","cli"
#              OR dict with list value containing those keys
#
#  Panel config keys:
#    "url"     – full API URL
#    "token"   – token / key value
#    "records" – number of records to fetch (default 20)
#    "api_type"– (auto-filled on first successful detect, stored in panels.json)
# ═══════════════════════════════════════════════════════════════

def _safe_json(r) -> Optional[Any]:
    """
    Safely parse a requests Response to JSON.
    Returns None on empty body, HTML, or any parse error.
    Never raises.
    """
    try:
        text = r.text.strip()
        if not text or text.startswith("<"):
            # Empty body or HTML page — not JSON
            return None
        return r.json()
    except Exception:
        return None


def _detect_api_type(cfg: dict) -> str:
    """
    Probe the panel endpoint and return one of:
      "old"  – original viewstats format
      "mo"   – MOAPI reseller/mdr.php format
      "ps"   – pscall.net smsreport format
      "unknown"

    Detection order:
      1. URL pattern match (fastest, zero network)
      2. PS API probe  (?key=)
      3. MO API probe  (?token= + dates)
      4. OLD API probe (?token=)

    Result is cached in cfg["api_type"] — only re-probes when "unknown".
    """
    if cfg.get("api_type") and cfg["api_type"] != "unknown":
        return cfg["api_type"]

    url   = cfg.get("url", "").lower()
    token = cfg.get("token", "")

    # ── 1. URL pattern fast-path ──────────────────────────────
    if "pscall.net" in url or "smsreport" in url:
        cfg["api_type"] = "ps"
        return "ps"
    if "reseller/mdr" in url or "moapi" in url:
        cfg["api_type"] = "mo"
        return "mo"
    if "viewstats" in url or "crapi" in url:
        cfg["api_type"] = "old"
        return "old"

    # ── 2. PS API probe (?key=) ───────────────────────────────
    try:
        base_url = cfg["url"].split("?")[0].rstrip("/")
        token    = cfg.get("token", "").strip()
        _ps_headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
            "Accept": "application/json, text/plain, */*",
            "Referer": "https://pscall.net/",
        }
        r = requests.get(f"{base_url}?key={token}", headers=_ps_headers, timeout=8)
        if r.status_code == 200:
            j = _safe_json(r)
            if j is not None:
                rows = j if isinstance(j, list) else (
                    j.get("data") or j.get("records") or []
                )
                if isinstance(rows, list):
                    # Even an empty list [] is a valid PS response
                    # Check first item if available, else trust URL returned valid JSON list
                    if not rows:
                        # Could be PS with no data today — check if it's a clean list
                        # (PS returns [] not {"status":"error"})
                        cfg["api_type"] = "ps"
                        return "ps"
                    first = rows[0]
                    if isinstance(first, dict) and (
                        "num" in first or "sms" in first or "dateadded" in first
                    ):
                        cfg["api_type"] = "ps"
                        return "ps"
    except Exception:
        pass

    # ── 3. MO API probe (?token= + dates) ────────────────────
    try:
        today  = datetime.now().strftime('%Y-%m-%d')
        params = {
            "token":        token,
            "fromdate":     f"{today} 00:00:00",
            "todate":       f"{today} 23:59:59",
            "records":      1,
            "searchnumber": "",
            "searchcli":    ""
        }
        r = requests.get(cfg["url"], params=params, timeout=8)
        if r.status_code == 200:
            j = _safe_json(r)
            if j is not None and isinstance(j, dict):
                status = str(j.get("status", ""))
                if "Success" in status or ("Error" in status and "token" in str(j).lower()):
                    cfg["api_type"] = "mo"
                    return "mo"
    except Exception:
        pass

    # ── 4. OLD API probe (?token=) ────────────────────────────
    try:
        r = requests.get(cfg["url"], params={"token": token, "records": 1}, timeout=8)
        if r.status_code == 200:
            j = _safe_json(r)
            if j is not None:
                if isinstance(j, dict) and j.get("status") in ("success", "Success"):
                    cfg["api_type"] = "old"
                    return "old"
                if isinstance(j, list):
                    cfg["api_type"] = "old"
                    return "old"
    except Exception:
        pass

    cfg["api_type"] = "unknown"
    return "unknown"


def _fetch_old_api(cfg: dict, limit: int) -> List[Dict]:
    """Fetch from original viewstats / crapi panel."""
    r = requests.get(
        cfg["url"],
        params={"token": cfg["token"], "records": limit},
        timeout=10
    )
    # Guard: empty or HTML response — return empty silently
    data = _safe_json(r)
    if data is None:
        logger.warning(f"OLD API [{cfg['url'][:40]}] — empty/non-JSON response, skipping")
        return []
    results = []
    if isinstance(data, dict) and data.get("status") in ("success", "Success"):
        for row in data.get("data", [])[:limit]:
            msg = row.get("message") or row.get("msg") or row.get("sms") or ""
            results.append({
                "time":    row.get("dt") or row.get("datetime") or row.get("dateadded") or "",
                "number":  row.get("num") or row.get("number") or "",
                "service": row.get("cli") or "Unknown",
                "message": msg
            })
    elif isinstance(data, list):
        for row in data[:limit]:
            if isinstance(row, dict):
                results.append({
                    "time":    row.get("dt") or row.get("datetime") or "",
                    "number":  row.get("num") or row.get("number") or "",
                    "service": row.get("cli") or "Unknown",
                    "message": row.get("message") or row.get("sms") or ""
                })
            elif isinstance(row, (list, tuple)) and len(row) >= 4:
                results.append({
                    "time":    row[3], "number": row[1],
                    "service": row[0] or "Unknown", "message": row[2]
                })
    return results


def _fetch_mo_api(cfg: dict, limit: int) -> List[Dict]:
    """Fetch from MOAPI reseller/mdr.php format."""
    today  = datetime.now().strftime('%Y-%m-%d')
    params = {
        "token":        cfg["token"],
        "fromdate":     f"{today} 00:00:00",
        "todate":       f"{today} 23:59:59",
        "records":      limit,
        "searchnumber": "",
        "searchcli":    ""
    }
    r    = requests.get(cfg["url"], params=params, timeout=10)
    data = _safe_json(r)
    if data is None:
        logger.warning(f"MO API [{cfg['url'][:40]}] — empty/non-JSON response, skipping")
        return []
    results = []
    if isinstance(data, dict) and "Success" in str(data.get("status", "")):
        for row in data.get("data", [])[:limit]:
            results.append({
                "time":    row.get("datetime") or row.get("dt") or "",
                "number":  row.get("number")   or row.get("num") or "",
                "service": row.get("cli") or "Unknown",
                "message": row.get("message") or row.get("sms") or ""
            })
    return results


def _fetch_ps_api(cfg: dict, limit: int) -> List[Dict]:
    """
    Fetch from pscall.net smsreport format.
    Uses browser User-Agent + raw key URL to bypass server IP restrictions.
    """
    base_url = cfg["url"].split("?")[0].rstrip("/")
    token    = cfg.get("token", "").strip()
    full_url = f"{base_url}?key={token}"
    headers  = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://pscall.net/",
    }
    r   = requests.get(full_url, headers=headers, timeout=10)
    raw = _safe_json(r)
    if raw is None:
        logger.warning(f"PS API [{base_url}?key=***] — empty/non-JSON response (HTTP {r.status_code}), skipping")
        return []
    logger.info(f"PS API [{base_url}] — got {len(raw) if isinstance(raw, list) else type(raw).__name__} records")
    # pscall returns a list directly or {"data":[...]}
    if isinstance(raw, list):
        rows = raw
    elif isinstance(raw, dict):
        rows = raw.get("data") or raw.get("records") or []
    else:
        rows = []
    results = []
    for row in rows:
        if not isinstance(row, dict):
            continue
        # Only forward successful records
        if str(row.get("cause", "Success")).lower() not in ("success", ""):
            continue
        results.append({
            "time":    row.get("dateadded") or row.get("datetime") or "",
            "number":  row.get("num") or row.get("number") or "",
            "service": row.get("cli") or "Unknown",
            "message": row.get("sms") or row.get("message") or ""
        })
    return results


def _fetch_universal(panel_name: str, limit: int = 20) -> List[Dict]:
    """
    Universal fetch: uses cached api_type for fast-path,
    falls back gracefully on error WITHOUT resetting the type
    (avoids infinite re-probe loops on flaky servers).
    """
    if panel_name not in API_PANELS:
        return []
    cfg      = API_PANELS[panel_name]
    api_type = _detect_api_type(cfg)

    # Persist detected type to panels.json
    panels = load_panels()
    if panel_name in panels and panels[panel_name].get("api_type") != cfg.get("api_type"):
        panels[panel_name]["api_type"] = cfg.get("api_type", "unknown")
        save_panels(panels)

    fetchers = {
        "old": _fetch_old_api,
        "mo":  _fetch_mo_api,
        "ps":  _fetch_ps_api,
    }

    if api_type in fetchers:
        try:
            rows = fetchers[api_type](cfg, limit)
            # Empty result is fine (no new OTPs) — do NOT reset type
            return rows
        except Exception as e:
            logger.error(f"[{panel_name}] {api_type.upper()} fetch error: {e}")
            # Do NOT reset cfg["api_type"] here — a temporary server
            # error (timeout, 500, etc.) should not trigger re-detection.
            # Only reset if we got a confirmed wrong-format response.
            return []

    # Type is "unknown" — try all three in order, pick first that returns data
    for name, fn in fetchers.items():
        try:
            rows = fn(cfg, limit)
            if rows:
                cfg["api_type"] = name
                logger.info(f"[{panel_name}] Auto-detected as {name.upper()} API")
                # Persist
                panels = load_panels()
                if panel_name in panels:
                    panels[panel_name]["api_type"] = name
                    save_panels(panels)
                return rows
        except Exception:
            continue
    return []


def fetch_latest(panel_name: str) -> Optional[Dict]:
    rows = fetch_latest_batch(panel_name, limit=1)
    return rows[0] if rows else None


def fetch_latest_batch(panel_name: str, limit: int = 20) -> List[Dict]:
    try:
        return _fetch_universal(panel_name, limit)
    except Exception as e:
        STATS["errors"] += 1
        logger.error(f"fetch_latest_batch error {panel_name}: {e}")
        return []


def fetch_all_panels(limit: int = 5) -> list:
    results = []
    for panel_name in list(API_PANELS.keys()):
        try:
            rows = _fetch_universal(panel_name, limit)
            for row in rows:
                row["panel"] = panel_name
                results.append(row)
        except Exception as e:
            logger.error(f"fetch_all_panels error {panel_name}: {e}")
    return results

# ═══════════════════════════════════════════════════════════════
#  EXCEPTION HANDLER
# ═══════════════════════════════════════════════════════════════
def handle_task_exception(task: asyncio.Task):
    try:
        task.result()
    except asyncio.CancelledError:
        pass
    except Exception as e:
        logger.error(f"Task {task.get_name()} exception: {e}", exc_info=True)

# ═══════════════════════════════════════════════════════════════
#  IVAS WEBSOCKET WORKER
# ═══════════════════════════════════════════════════════════════
async def _ivas_ping(ws, interval_ms):
    while True:
        await asyncio.sleep(interval_ms / 1000)
        try:
            await ws.send("3")
        except:
            break

async def ivas_worker(name: str):
    logger.info(f"🔌 IVAS worker starting: {name}")
    seen = set()
    while True:
        try:
            accounts = load_ivas()
            if name not in accounts:
                logger.info(f"IVAS '{name}' removed — stopping.")
                break
            uri = accounts[name].get("uri", "")
            if not uri:
                await asyncio.sleep(10)
                continue
            ssl_ctx = ssl._create_unverified_context()
            try:
                async with websockets.connect(uri, ssl=ssl_ctx) as ws:
                    logger.info(f"✅ IVAS [{name}] connected.")
                    initial = await ws.recv()
                    ping_interval = 25000
                    try:
                        if initial.startswith("0{"):
                            ping_interval = json.loads(initial[1:]).get("pingInterval", 25000)
                    except:
                        pass
                    await ws.send("40/livesms,")
                    ping_task = asyncio.create_task(_ivas_ping(ws, ping_interval))
                    try:
                        check_counter = 0
                        while True:
                            check_counter += 1
                            if check_counter % 100 == 0:
                                if name not in load_ivas():
                                    break
                            msg = await ws.recv()
                            if not msg.startswith("42/livesms,"):
                                continue
                            try:
                                data = json.loads(msg[msg.find("["):])
                                if not (isinstance(data, list) and len(data) > 1
                                        and isinstance(data[1], dict)):
                                    continue
                                sms     = data[1]
                                number  = sms.get("recipient", "")
                                text    = sms.get("message", "") or ""
                                service = sms.get("originator", "Unknown")
                                country = sms.get("range", "")
                                otp     = extract_otp(text)
                                uniq    = f"{number}-{text[:20]}"
                                if uniq in seen:
                                    continue
                                seen.add(uniq)
                                if len(seen) > 1000:
                                    seen = set(list(seen)[-500:])
                                STATS["ivas_hits"][name] = STATS["ivas_hits"].get(name, 0) + 1
                                log_otp_memory(number, service, otp, f"IVAS:{name}")
                                if otp and number:
                                    store = load_otp_store()
                                    store[number] = {"otp": otp, "ts": time.time(), "service": service}
                                    save_otp_store(store)
                                formatted = format_otp_message(number, service, otp or "N/A",
                                    source_label=f"IVAS:{name}", sms_text=text)
                                keyboard = get_otp_keyboard(number, otp)
                                await send_to_all_groups(formatted, reply_markup=keyboard)
                                if otp:
                                    await send_otp_to_owner(number, service, otp,
                                        sms_text=text, source_label=f"IVAS:{name}")
                            except Exception as e:
                                logger.error(f"IVAS [{name}] parse error: {e}")
                    finally:
                        ping_task.cancel()
            except websockets.exceptions.WebSocketException as e:
                logger.error(f"IVAS [{name}] WS error: {e}. Retry in 5s...")
                await asyncio.sleep(5)
            except Exception as e:
                logger.error(f"IVAS [{name}] error: {e}. Retry in 5s...")
                await asyncio.sleep(5)
        except Exception as e:
            logger.error(f"IVAS [{name}] critical: {e}. Retry in 10s...")
            await asyncio.sleep(10)

# ═══════════════════════════════════════════════════════════════
#  REST API WORKER
# ═══════════════════════════════════════════════════════════════
async def api_worker(panel: str):
    seen: set = set()
    logger.info(f"📡 REST worker starting: {panel}")
    loop = asyncio.get_event_loop()
    while True:
        try:
            if panel not in API_PANELS:
                break
            rows = await loop.run_in_executor(None, lambda: fetch_latest_batch(panel, limit=20))
            for data in rows:
                uniq = f"{data['number']}-{data['message'][:30]}"
                if uniq in seen:
                    continue
                seen.add(uniq)
                if len(seen) > 1000:
                    seen = set(list(seen)[-500:])
                otp = extract_otp(data["message"])
                STATS["panel_hits"][panel] = STATS["panel_hits"].get(panel, 0) + 1
                log_otp_memory(data["number"], data["service"], otp, f"REST:{panel}")
                if otp and data["number"]:
                    store = load_otp_store()
                    store[data["number"]] = {"otp": otp, "ts": time.time(), "service": data.get("service", "Unknown")}
                    save_otp_store(store)
                formatted = format_otp_message(
                    data["number"], data["service"], otp or "N/A",
                    source_label=f"REST:{panel}", sms_text=data.get("message", ""))
                keyboard = get_otp_keyboard(data["number"], otp)
                await send_to_all_groups(formatted, reply_markup=keyboard)
                if otp:
                    await send_otp_to_owner(data["number"], data["service"], otp,
                        sms_text=data.get("message",""), source_label=f"REST:{panel}")
        except Exception as e:
            logger.error(f"REST worker error {panel}: {e}")
        await asyncio.sleep(2)

# ═══════════════════════════════════════════════════════════════
#  MONITOR & CLEANUP
# ═══════════════════════════════════════════════════════════════
async def monitor_tasks():
    while True:
        await asyncio.sleep(60)
        for name in load_ivas():
            if name not in IVAS_TASKS or IVAS_TASKS[name].done():
                logger.warning(f"IVAS '{name}' dead — restarting...")
                task = asyncio.create_task(ivas_worker(name), name=f"IVAS-{name}")
                task.add_done_callback(handle_task_exception)
                IVAS_TASKS[name] = task
        for panel in list(API_PANELS.keys()):
            if panel not in REST_TASKS or REST_TASKS[panel].done():
                logger.warning(f"REST '{panel}' dead — restarting...")
                task = asyncio.create_task(api_worker(panel), name=f"REST-{panel}")
                task.add_done_callback(handle_task_exception)
                REST_TASKS[panel] = task

async def cleanup_states():
    while True:
        await asyncio.sleep(60)
        now = time.time()
        for d in [PANEL_ADD_STATES, IVAS_ADD_STATES, BROADCAST_STATES,
                  SETTING_STATES, FETCH_STATES]:
            for uid in list(d.keys()):
                if now - d[uid].get("timestamp", 0) > STATE_TIMEOUT:
                    del d[uid]

# ═══════════════════════════════════════════════════════════════
#  KEYBOARDS
# ═══════════════════════════════════════════════════════════════
def b(text, cb=None, url=None):
    return InlineKeyboardButton(text, callback_data=cb) if cb else InlineKeyboardButton(text, url=url)

def bc(text, cb=None, url=None, style=None):
    """Button with optional Bot API 9.4 color style."""
    kwargs = {}
    if style:
        kwargs["api_kwargs"] = {"style": style}
    if cb:
        return InlineKeyboardButton(text, callback_data=cb, **kwargs)
    return InlineKeyboardButton(text, url=url, **kwargs)

def get_main_menu_keyboard():
    return InlineKeyboardMarkup([
        [
            bc("🧇 𝗚𝗲𝘁 𝗡𝘂𝗺𝗯𝗲𝗿",  cb="show_countries",               style="success"),
            bc("🫁 𝗣𝗿𝗼𝗳𝗶𝗹𝗲",       cb="user_profile",                style="primary"),
        ],
        [
            bc("🧠 𝗗𝗲𝘃𝗲𝗹𝗼𝗽𝗲𝗿",     url="https://t.me/Samiorbit",     style="danger"),
        ],
    ])

def get_join_keyboard():
    return InlineKeyboardMarkup([
        [bc("📞 BlazeNXT Numbers",    url="https://t.me/blazenxt_numbers",      style="danger")],
        [bc("💬 WhatsApp Group",  url="https://chat.whatsapp.com/HVqCQ6wX0sz9sqox5QEgrg?mode=hqctcla",  style="primary")],
        [bc("📲 BlazeNXT OTP",        url="https://t.me/+DfUnv_qgZEFkZWU8",      style="success")],
        [bc("✅ I Joined — Check", cb="check_join",                    style="success")],
    ])

def get_admin_keyboard(uid: int = 0):
    """Build admin panel buttons based on permissions — each button has its own colour"""
    rows = []
    row = []
    if has_perm(uid, "numbers"): row.append(bc("📦 Numbers",   cb="menu_numbers",     style="success"))
    if has_perm(uid, "files"):   row.append(bc("📂 Files",     cb="menu_files",       style="primary"))
    if row: rows.append(row)
    row = []
    if has_perm(uid, "panels"):  row.append(bc("📡 Panels",    cb="menu_panels",      style="primary"))
    if has_perm(uid, "ivas"):    row.append(bc("🔌 IVAS",      cb="menu_ivas",        style="success"))
    if row: rows.append(row)
    row = []
    if has_perm(uid, "fetch_sms"):   row.append(bc("🔄 Fetch SMS",   cb="menu_fetch",        style="primary"))
    if has_perm(uid, "otp_history"): row.append(bc("📋 OTP History", cb="menu_otp_history",  style="success"))
    if row: rows.append(row)
    row = []
    if has_perm(uid, "groups"):    row.append(bc("👥 Groups",    cb="menu_groups",    style="primary"))
    if has_perm(uid, "broadcast"): row.append(bc("📢 Broadcast", cb="broadcast",      style="danger"))
    if row: rows.append(row)
    row = []
    if has_perm(uid, "settings"):  row.append(bc("⚙️ Settings",  cb="menu_settings",  style="primary"))
    if has_perm(uid, "advanced"):  row.append(bc("🔧 Advanced",  cb="menu_advanced",  style="danger"))
    if row: rows.append(row)
    if has_perm(uid, "stats"):
        rows.append([
            bc("📊 Stats",  cb="stats",  style="success"),
            bc("📡 Status", cb="status", style="primary"),
        ])
    rows.append([
        bc("🔄 Refresh", cb="refresh_admin", style="primary"),
        bc("❌ Close",   cb="close_admin",   style="danger"),
    ])
    return InlineKeyboardMarkup(rows)

def get_numbers_menu():
    return InlineKeyboardMarkup([
        [b("➕ Add Numbers","nb_add_numbers"),  b("📋 View Stock","nb_number_list")],
        [b("🗑️ Delete Country","nb_delete_menu"),b("📤 Export","nb_export")],
        [b("📊 Stock Stats","nb_stock_stats"),  b("🔙 Back","back_to_admin")],
    ])

def get_files_menu():
    return InlineKeyboardMarkup([
        [b("📂 List Files","fm_list"),          b("📥 Download Log","fm_download_log")],
        [b("📥 Download OTP Store","fm_download_otp"),b("📥 Download DB","fm_download_db")],
        [b("🗑️ Clear Log","fm_clear_log"),      b("🔙 Back","back_to_admin")],
    ])

def get_panels_menu():
    return InlineKeyboardMarkup([
        [b("📋 List Panels","list_panels"),     b("➕ Add Panel","add_panel")],
        [b("🗑️ Remove Panel","remove_panel"),  b("🧪 Test All","test_panels_menu")],
        [b("🔄 Fetch Latest","panel_fetch_all"),b("🔙 Back","back_to_admin")],
    ])

def get_panels_keyboard(action="view"):
    panels  = load_panels()
    keyboard = []
    for name in panels:
        active = (name in REST_TASKS and not REST_TASKS[name].done())
        st     = "🟢" if active else "🔴"
        cb     = f"remove_panel_{name}" if action == "remove" else f"view_panel_{name}"
        label  = f"{st} {name.upper()}" + (" 🗑️" if action == "remove" else "")
        keyboard.append([b(label, cb)])
    keyboard.append([b("🔙 Back","menu_panels")])
    return InlineKeyboardMarkup(keyboard)

def get_ivas_menu():
    return InlineKeyboardMarkup([
        [b("📋 List IVAS","list_ivas"),         b("➕ Add IVAS","add_ivas")],
        [b("🗑️ Remove IVAS","remove_ivas"),     b("🔄 Restart All","ivas_restart_all")],
        [b("🔙 Back","back_to_admin")],
    ])

def get_ivas_keyboard(action="view"):
    accounts = load_ivas()
    keyboard = []
    for name in accounts:
        active = (name in IVAS_TASKS and not IVAS_TASKS[name].done())
        st     = "🟢" if active else "🔴"
        cb     = f"remove_ivas_{name}" if action == "remove" else f"view_ivas_{name}"
        label  = f"{st} {name.upper()}" + (" 🗑️" if action == "remove" else "")
        keyboard.append([b(label, cb)])
    keyboard.append([b("🔙 Back","menu_ivas")])
    return InlineKeyboardMarkup(keyboard)

def get_groups_menu():
    groups  = load_groups()
    config  = load_config()
    keyboard = []
    for gid in groups:
        keyboard.append([b(f"🗑️ Remove {gid}", f"del_group_{gid}")])
    keyboard.append([b("➕ Add Group","add_group_prompt")])
    keyboard.append([b("📋 Set Log Group","set_log_group"),
                     b("❌ Clear Log Group","clear_log_group")])
    keyboard.append([b("🔙 Back","back_to_admin")])
    return InlineKeyboardMarkup(keyboard)

def get_otp_history_menu():
    return InlineKeyboardMarkup([
        [b("📋 Last 10","otp_hist_10"),         b("📋 Last 20","otp_hist_20")],
        [b("🔍 Search by Number","otp_search_num"),b("📤 Export CSV","otp_export_hist")],
        [b("🗑️ Clear History","otp_clear_hist"),b("🔙 Back","back_to_admin")],
    ])

def get_fetch_menu():
    return InlineKeyboardMarkup([
        [b("🔄 Fetch All Panels","fetch_all_now")],
        [b("🔍 Fetch by Number","fetch_by_number")],
        [b("📡 Fetch Single Panel","fetch_single_panel")],
        [b("🔙 Back","back_to_admin")],
    ])

def get_settings_menu():
    config = load_config()
    fwd    = "✅ ON" if config.get("otp_forward", True) else "❌ OFF"
    delay  = config.get("forward_delay", 0)
    lg     = str(config.get("log_group") or "None")[:12]
    return InlineKeyboardMarkup([
        [b(f"📤 OTP Forward: {fwd}","toggle_otp_forward")],
        [b(f"⏱ Delay: {delay}s","set_forward_delay"),
         b("📢 Channel Link","set_channel")],
        [b("🤖 NumberBot Link","set_numberbot"),
         b(f"📋 Log Group: {lg}","set_log_group")],
        [b("🔗 OTP Group Link","set_otp_group_link"),
         b("👤 Admin Manager","menu_admin_manager")],
        [b("🔙 Back","back_to_admin")],
    ])

def get_admin_manager_keyboard():
    staff    = load_staff()
    keyboard = []
    for aid in OWNER_IDS:
        keyboard.append([b(f"👑 {aid}  (Owner)", "noop")])
    for uid_str, info in staff.items():
        uid_int = int(uid_str)
        if uid_int in OWNER_IDS:
            continue
        name  = info.get("name", uid_str)
        perms = info.get("perms", [])
        keyboard.append([
            b(f"🛡️ {name} ({len(perms)} perms)", f"edit_staff_{uid_str}"),
            b("🗑️", f"remove_staff_{uid_str}")
        ])
    keyboard.append([b("➕ Add Staff Member", "add_staff_prompt")])
    keyboard.append([b("🔙 Back", "menu_settings")])
    return InlineKeyboardMarkup(keyboard)

def get_staff_perms_keyboard(uid_str: str):
    staff   = load_staff()
    info    = staff.get(uid_str, {})
    cur     = info.get("perms", [])
    keyboard = []
    for perm_key, perm_label in ALL_PERMISSIONS.items():
        has = perm_key in cur
        icon = "✅" if has else "☑️"
        keyboard.append([b(f"{icon} {perm_label}", f"toggle_perm_{uid_str}_{perm_key}")])
    keyboard.append([
        b("✅ Grant All",  f"grant_all_{uid_str}"),
        b("❌ Revoke All", f"revoke_all_{uid_str}")
    ])
    keyboard.append([b("🔙 Back", "menu_admin_manager")])
    return InlineKeyboardMarkup(keyboard)

def get_advanced_keyboard():
    return InlineKeyboardMarkup([
        [b("🔄 Restart All Workers","restart_workers"),
         b("🛑 Stop Forwarding","stop_forward")],
        [b("▶️ Start Forwarding","start_forward"),
         b("🔄 Reload Config","reload_config")],
        [b("🗑️ Clear OTP Store","clear_all_otps"),
         b("📤 Export OTP Store","export_otps")],
        [b("📋 View Logs","view_logs"),
         b("🔁 Restart Bot","restart_bot")],
        [b("🧪 Test All Panels","test_panels_adv"),
         b("📊 Worker Status","worker_status")],
        [b("🔙 Back","back_to_admin")],
    ])

def get_confirmation_keyboard(action: str, extra: str = ""):
    cd = f"confirm_{action}" + (f"_{extra}" if extra else "")
    return InlineKeyboardMarkup([
        [b("✅ Confirm", cd), b("❌ Cancel","cancel_action")]
    ])

def get_broadcast_keyboard():
    return InlineKeyboardMarkup([
        [b("📝 Text Only","broadcast_text"),
         b("🔘 With Buttons","broadcast_with_buttons")],
        [b("🔙 Back","back_to_admin")]
    ])

def get_countries_keyboard():
    rows = db_get_countries()
    if not rows:
        return None
    # Use custom emojis for country buttons
    buttons = []
    for c, n in rows:
        region_code = c[:2].upper() if len(c) >= 2 else "DEFAULT"
        custom_emoji = get_custom_country_emoji(region_code)
        # Strip HTML tags for button text, just show emoji representation
        emoji_display = "🌍"  # fallback
        buttons.append(b(f"{emoji_display} {c} ({n})", f"nb_get|{c}"))
    kb = [buttons[i:i+2] for i in range(0, len(buttons), 2)]
    kb.append([b("🔄 Refresh","show_countries")])
    return InlineKeyboardMarkup(kb)

def get_nb_stock_keyboard():
    rows     = db_get_countries()
    keyboard = [[b(f"❌ {c} ({n})  Delete", f"nb_del|{c}")] for c, n in rows]
    keyboard.append([b("🔙 Back","menu_numbers")])
    return InlineKeyboardMarkup(keyboard)

# ═══════════════════════════════════════════════════════════════
#  COMMANDS
# ═══════════════════════════════════════════════════════════════

async def check_join(bot, uid: int) -> bool:
    for ch in REQUIRED_CHANNELS:
        ch_id = ch.get("id")
        if not ch_id:
            continue
        try:
            member = await bot.get_chat_member(ch_id, uid)
            if member.status in ("left", "kicked"):
                return False
        except Exception:
            return False
    return True

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    from html import escape
    uid   = update.effective_user.id
    first = escape(update.effective_user.first_name or "User")
    db_add_user(uid)

    if not is_admin(uid):
        joined = await check_join(context.bot, uid)
        if not joined:
            await update.message.reply_text(
                f"👋 <b>HI {first}</b>\n"
                f"━━━━━━━━━━━━━━━━━━━━━━\n\n"
                f"⚠️ <b>Join required channels first!</b>\n\n"
                f"Please join all channels below then tap <b>I Joined</b>.",
                parse_mode="HTML",
                reply_markup=get_join_keyboard())
            return

    msg = (
        f"👋 <b>HI {first}</b>\n"
        f"━━━━━━━━━━━━━━━━━━━━━━\n\n"
        f"💎 <b>BLAZENXT BOT</b>\n"
        f"⚡ Fastest OTP Service\n"
        f"🤖 Auto-Assign System\n"
        f"🧬 Multi-Panel + IVAS Support\n\n"
        f"🆔 <b>Version :</b> 7.0\n\n"
        f"👆 <b>Select an option:</b>"
    )
    if is_admin(uid):
        msg += "\n\n🛡️ <b>ADMIN</b> — /admin"
    await update.message.reply_text(msg, parse_mode="HTML",
                                    reply_markup=get_main_menu_keyboard())

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        f"🔔 <b>{BOT_NAME}</b> - Help\n━━━━━━━━━━━━━━━━━━━━━━\n"
        f"/start — Start\n/admin — Admin panel\n"
        f"/otpfor [num] — Search OTP\n/fetchsms — Fetch latest SMS\n"
        f"/status — Bot status\n/stats — Statistics\n"
        f"/addgroup [id] — Add OTP group\n/removegroup [id] — Remove group\n"
        f"/reload — Reload workers\n"
        f"━━━━━━━━━━━━━━━━━━━━━━\n🤖 Dev: {DEV_CONTACT}",
        parse_mode="HTML", reply_markup=get_main_menu_keyboard())

async def admin_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    if is_admin(uid):
        await update.message.reply_text(
            f"💎 <b>ADMIN PANEL</b>\n━━━━━━━━━━━━━━━━━━━━━━\nSelect option:",
            parse_mode="HTML", reply_markup=get_admin_keyboard(uid))
    else:
        await update.message.reply_text("❌ Unauthorized!")

async def otpfor_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("❌ Use: /otpfor 447123456789")
        return
    target = context.args[0].replace("+", "")
    wait   = await update.message.reply_text(f"🔄 Scanning <code>{target}</code>...", parse_mode="HTML")
    found  = None
    store  = load_otp_store()
    for k, v in store.items():
        if target in k:
            found = v
            break
    if not found:
        rows = db_search_otp_by_number(target)
        if rows:
            found = rows[0][2]
    if not found:
        for panel in API_PANELS:
            d2 = fetch_latest(panel)
            if d2 and target in d2["number"]:
                found = extract_otp(d2["message"])
                if found:
                    break
    if found:
        await wait.edit_text(
            f"✅ <b>OTP FOUND</b>\n━━━━━━━━━━━━━━━━━━━━━━\n"
            f"📞 <code>{target}</code>\n🔑 <code>{found}</code>", parse_mode="HTML")
    else:
        await wait.edit_text(
            f"❌ <b>No OTP found</b> for <code>{target}</code>", parse_mode="HTML")

async def fetchsms_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id):
        await update.message.reply_text("❌ Unauthorized!")
        return
    wait    = await update.message.reply_text("🔄 Fetching...")
    results = await asyncio.get_running_loop().run_in_executor(None, fetch_all_panels, 5)
    if not results:
        await wait.edit_text("❌ No SMS fetched.")
        return
    text = f"📨 <b>LATEST SMS ({len(results)})</b>\n━━━━━━━━━━━━━━━━━━━━━━\n"
    for r in results[:10]:
        otp  = extract_otp(r["message"]) or "N/A"
        text += (f"\n📡 <b>{r['panel']}</b> | {r['service']}\n"
                 f"📞 <code>{r['number']}</code>\n"
                 f"🔑 OTP: <code>{otp}</code>\n"
                 f"💬 {r['message'][:80]}\n──────────────────────\n")
    await wait.edit_text(text[:4000], parse_mode="HTML")

async def status_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id):
        await update.message.reply_text("❌ Unauthorized!")
        return
    await update.message.reply_text(_build_status(), parse_mode="HTML")

async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id):
        await update.message.reply_text("❌ Unauthorized!")
        return
    total, active_today, active_week = db_user_stats()
    uptime = str(datetime.now() - datetime.fromtimestamp(STATS['start_time'])).split('.')[0]
    await update.message.reply_text(
        f"📊 <b>BOT STATS</b>\n━━━━━━━━━━━━━━━━━━━━━━\n"
        f"⏱ Uptime: <code>{uptime}</code>\n"
        f"👤 Total Users: <code>{total}</code>\n"
        f"🟢 Active Today: <code>{active_today}</code>\n"
        f"📅 This Week: <code>{active_week}</code>\n"
        f"📊 OTPs Sent: <code>{STATS['otps_sent']}</code>\n"
        f"🚫 Dropped: <code>{STATS['otps_dropped']}</code>\n"
        f"❌ Errors: <code>{STATS['errors']}</code>\n"
        f"📦 Numbers in DB: <code>{db_total_numbers()}</code>\n"
        f"🗄 OTP Store: <code>{len(load_otp_store())}</code>\n"
        f"📡 REST Panels: <code>{len(load_panels())}</code>\n"
        f"🔌 IVAS Accounts: <code>{len(load_ivas())}</code>\n"
        f"━━━━━━━━━━━━━━━━━━━━━━", parse_mode="HTML")

async def addgroup_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id):
        await update.message.reply_text("❌ Unauthorized!")
        return
    if not context.args:
        await update.message.reply_text("Usage: /addgroup <chat_id>")
        return
    try:
        gid    = int(context.args[0])
        groups = load_groups()
        if gid in groups:
            await update.message.reply_text("🟡 Already exists.")
            return
        groups.append(gid)
        save_groups(groups)
        await update.message.reply_text(f"✅ Group <code>{gid}</code> added.", parse_mode="HTML")
    except ValueError:
        await update.message.reply_text("❌ Invalid chat ID.")

async def removegroup_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id):
        await update.message.reply_text("❌ Unauthorized!")
        return
    if not context.args:
        await update.message.reply_text("Usage: /removegroup <chat_id>")
        return
    try:
        gid    = int(context.args[0])
        groups = load_groups()
        if gid not in groups:
            await update.message.reply_text("❌ Not found.")
            return
        groups.remove(gid)
        save_groups(groups)
        await update.message.reply_text("✅ Group removed.")
    except ValueError:
        await update.message.reply_text("❌ Invalid chat ID.")

async def reload_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id):
        await update.message.reply_text("❌ Unauthorized!")
        return
    await _restart_all_workers()
    await update.message.reply_text(
        f"✅ Reloaded — REST: {len(API_PANELS)}, IVAS: {len(load_ivas())}, Groups: {len(load_groups())}")

async def do_broadcast(bot, message: str, keyboard=None) -> dict:
    """Send message to ALL users in DB. Returns stats dict."""
    c = db.cursor()
    c.execute("SELECT user_id FROM tg_users")
    user_ids = [row[0] for row in c.fetchall()]
    success = 0
    fail = 0
    for uid in user_ids:
        try:
            await bot.send_message(
                chat_id=uid, text=message,
                parse_mode="HTML", reply_markup=keyboard)
            success += 1
            await asyncio.sleep(0.05)  # avoid flood
        except Exception:
            fail += 1
    return {"total": len(user_ids), "success": success, "fail": fail}

async def broadcast_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id):
        await update.message.reply_text("❌ Unauthorized!")
        return
    if not context.args:
        await update.message.reply_text("Usage: /broadcast <message>")
        return
    wait = await update.message.reply_text("📢 Broadcasting...")
    stats = await do_broadcast(context.bot, " ".join(context.args))
    await wait.edit_text(
        f"📢 <b>BROADCAST COMPLETE</b>\n"
        f"━━━━━━━━━━━━━━━━━━━━━━\n"
        f"👥 Total Users: <code>{stats['total']}</code>\n"
        f"✅ Success: <code>{stats['success']}</code>\n"
        f"❌ Failed: <code>{stats['fail']}</code>",
        parse_mode="HTML")

# ═══════════════════════════════════════════════════════════════
#  INTERNAL HELPERS
# ═══════════════════════════════════════════════════════════════
def _build_status() -> str:
    uptime = str(datetime.now() - datetime.fromtimestamp(STATS['start_time'])).split('.')[0]
    config = load_config()
    fwd_st = "✅ ON" if config.get("otp_forward", True) else "❌ OFF"
    panels = load_panels()
    ivas   = load_ivas()
    plines = "\n".join([
        f"  {'🟢' if (p in REST_TASKS and not REST_TASKS[p].done()) else '🔴'} "
        f"{p} (hits:{STATS['panel_hits'].get(p,0)})"
        for p in panels]) or "  None"
    ilines = "\n".join([
        f"  {'🟢' if (n in IVAS_TASKS and not IVAS_TASKS[n].done()) else '🔴'} "
        f"{n} (hits:{STATS['ivas_hits'].get(n,0)})"
        for n in ivas]) or "  None"
    return (
        f"🖥 <b>BOT STATUS</b>\n━━━━━━━━━━━━━━━━━━━━━━\n"
        f"⏱ Uptime: <code>{uptime}</code>\n"
        f"📊 OTPs Sent: <code>{STATS['otps_sent']}</code>\n"
        f"❌ Errors: <code>{STATS['errors']}</code>\n"
        f"📤 Forward: {fwd_st} | Groups: {len(load_groups())}\n"
        f"━━━━━━━━━━━━━━━━━━━━━━\n"
        f"📡 <b>REST Panels:</b>\n{plines}\n"
        f"━━━━━━━━━━━━━━━━━━━━━━\n"
        f"🔌 <b>IVAS Accounts:</b>\n{ilines}\n"
        f"━━━━━━━━━━━━━━━━━━━━━━"
    )

async def _restart_all_workers():
    global API_PANELS
    API_PANELS = load_panels()
    for panel in list(REST_TASKS.keys()):
        REST_TASKS[panel].cancel()
        del REST_TASKS[panel]
    for panel in API_PANELS:
        task = asyncio.create_task(api_worker(panel), name=f"REST-{panel}")
        task.add_done_callback(handle_task_exception)
        REST_TASKS[panel] = task
    for name in list(IVAS_TASKS.keys()):
        IVAS_TASKS[name].cancel()
        del IVAS_TASKS[name]
    for name in load_ivas():
        task = asyncio.create_task(ivas_worker(name), name=f"IVAS-{name}")
        task.add_done_callback(handle_task_exception)
        IVAS_TASKS[name] = task

# ═══════════════════════════════════════════════════════════════
#  CALLBACK QUERY HANDLER
# ═══════════════════════════════════════════════════════════════
async def callback_query_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global API_PANELS
    query = update.callback_query
    await query.answer()
    uid  = query.from_user.id
    data = query.data

    if data == "noop":
        return

    # ── Public ────────────────────────────────────────────────
    if data.startswith("copy_"):
        await query.answer(f"🔑 {data[5:]}", show_alert=True)
        return

    if data == "show_help":
        await help_command(update, context)
        return

    if data == "public_stats":
        total, today, _ = db_user_stats()
        await query.edit_message_text(
            f"📊 <b>PUBLIC STATS</b>\n━━━━━━━━━━━━━━━━━━━━━━\n"
            f"Users: {total} | Active Today: {today}\n"
            f"OTPs in DB: {len(load_otp_store())}\n"
            f"Numbers: {db_total_numbers()}\n"
            f"━━━━━━━━━━━━━━━━━━━━━━", parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup([[b("🔙 Back","back_to_main")]]))
        return

    if data == "search_otp":
        await query.edit_message_text(
            "ℹ️ Use: <code>/otpfor [number]</code>", parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup([[b("🔙 Back","back_to_main")]]))
        return

    if data == "user_profile":
        from html import escape
        user       = query.from_user
        first      = escape(user.first_name or "")
        last       = escape(user.last_name or "")
        username   = f"@{user.username}" if user.username else "N/A"
        uid_val    = user.id
        c_cur = db.cursor()
        c_cur.execute("SELECT first_seen, last_seen, total_commands FROM tg_users WHERE user_id=?",
                      (uid_val,))
        row    = c_cur.fetchone()
        joined = row[0][:10] if row else "Unknown"
        cmds   = row[2] if row else 0
        total_users, today_u, _ = db_user_stats()
        await query.edit_message_text(
            f"🫁 <b>YOUR PROFILE</b>\n"
            f"━━━━━━━━━━━━━━━━━━━━━━\n"
            f"👤 <b>Name:</b> {first} {last}\n"
            f"🔖 <b>Username:</b> {username}\n"
            f"🆔 <b>User ID:</b> <code>{uid_val}</code>\n"
            f"📅 <b>Joined:</b> {joined}\n"
            f"📊 <b>Commands Used:</b> {cmds}\n"
            f"━━━━━━━━━━━━━━━━━━━━━━\n"
            f"📦 <b>Numbers Available:</b> {db_total_numbers()}\n"
            f"👥 <b>Total Bot Users:</b> {total_users}\n"
            f"━━━━━━━━━━━━━━━━━━━━━━",
            parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup([[b("🔙 𝗕𝗮𝗰𝗸", "back_to_main")]]))
        return

    if data == "back_to_main":
        from html import escape
        first = escape(query.from_user.first_name or "User")
        msg = (
            f"👋 <b>HI {first}</b>\n"
            f"━━━━━━━━━━━━━━━━━━━━━━\n\n"
            f"💎 <b>BLAZENXT BOT</b>\n"
            f"⚡ Fastest OTP Service\n"
            f"🤖 Auto-Assign System\n"
            f"🧬 Multi-Panel + IVAS Support\n\n"
            f"🆔 <b>Version :</b> 7.0\n\n"
            f"👆 <b>Select an option:</b>"
        )
        if is_admin(query.from_user.id):
            msg += "\n\n🛡️ <b>ADMIN</b> — /admin"
        await query.edit_message_text(msg, parse_mode="HTML",
                                      reply_markup=get_main_menu_keyboard())
        return

    if data == "check_join":
        from html import escape
        cb_uid = query.from_user.id
        joined = await check_join(context.bot, cb_uid)
        if joined:
            first = escape(query.from_user.first_name or "User")
            msg = (
                f"👋 <b>HI {first}</b>\n"
                f"━━━━━━━━━━━━━━━━━━━━━━\n\n"
                f"💎 <b>BLAZENXT BOT</b>\n"
                f"⚡ Fastest OTP Service\n"
                f"🤖 Auto-Assign System\n"
                f"🧬 Multi-Panel + IVAS Support\n\n"
                f"🆔 <b>Version :</b> 7.0\n\n"
                f"👆 <b>Select an option:</b>"
            )
            if is_admin(cb_uid):
                msg += "\n\n🛡️ <b>ADMIN</b> — /admin"
            await query.edit_message_text(msg, parse_mode="HTML",
                                          reply_markup=get_main_menu_keyboard())
        else:
            await query.answer("❌ You haven't joined all channels yet!", show_alert=True)
        return

    if data == "show_countries":
        rows = db_get_countries()
        if not rows:
            await query.edit_message_text("❌ No numbers available.",
                reply_markup=InlineKeyboardMarkup([[b("🔙 Back","back_to_main")]]))
            return
        await query.edit_message_text("🌍 <b>Select Country:</b>",
            parse_mode="HTML", reply_markup=get_countries_keyboard())
        return

    if data.startswith("nb_get|"):
        country = data.split("|", 1)[1]
        phones  = db_pop_numbers(country, 3)
        if phones:
            remaining = db_get_countries()
            rem_count = next((n for c, n in remaining if c == country), 0)

            db_assign_numbers(uid, phones)

            num_lines = ""
            for i, ph in enumerate(phones, 1):
                num_lines += f"📱 <b>0{i}</b>  ›  <code>{ph}</code>\n"

            msg = (
                f"🌍 <b>YOUR NUMBERS</b>\n"
                f"━━━━━━━━━━━━━━━━━━━━━━\n"
                f"🌍 <b>Country:</b> {country}\n"
                f"📦 <b>Remaining:</b> {rem_count}\n"
                f"━━━━━━━━━━━━━━━━━━━━━━\n"
                f"{num_lines}"
                f"━━━━━━━━━━━━━━━━━━━━━━\n"
                f"⏳ <b>Waiting for OTP...</b>\n"
                f"🔔 OTP will be sent here and in the group!"
            )
            await query.edit_message_text(
                msg,
                parse_mode="HTML",
                reply_markup=InlineKeyboardMarkup([
                    [b("🔄 Get 3 More Numbers", f"nb_get|{country}"),
                     b("🌍 Change Country",      "show_countries")],
                    [b("📢 BlazeNXT OTP Group", url="https://t.me/+DfUnv_qgZEFkZWU8")],
                    [b("🔙 Back",               "back_to_main")],
                ]))
        else:
            await query.answer("❌ Out of stock!", show_alert=True)
        return

    # ── Admin gate ────────────────────────────────────────────
    if not is_admin(uid):
        await query.edit_message_text("❌ Unauthorized!")
        return

    # ── Admin nav ─────────────────────────────────────────────
    if data in ("back_to_admin", "refresh_admin"):
        await query.edit_message_text(
            "💎 <b>ADMIN PANEL</b>\n━━━━━━━━━━━━━━━━━━━━━━\nSelect option:",
            parse_mode="HTML", reply_markup=get_admin_keyboard(uid))
        return

    if data == "close_admin":
        await query.delete_message()
        return

    # ══ NUMBERS ═══════════════════════════════════════════════
    if data == "menu_numbers":
        if not has_perm(uid,"numbers"): await query.answer("❌ No permission.",show_alert=True); return
        rows  = db_get_countries()
        total = db_total_numbers()
        lines = "\n".join([f"  {c}: <b>{n}</b>" for c,n in rows]) or "  Empty"
        await query.edit_message_text(
            f"📦 <b>NUMBER MANAGER</b>\n━━━━━━━━━━━━━━━━━━━━━━\nTotal: <b>{total}</b>\n\n{lines}",
            parse_mode="HTML", reply_markup=get_numbers_menu())
        return

    if data == "nb_add_numbers":
        NB_STATE[uid] = {"step": "waiting_country", "timestamp": time.time()}
        await query.edit_message_text(
            "📦 <b>ADD NUMBERS</b>\n━━━━━━━━━━━━━━━━━━━━━━\nSend the <b>Country Name</b>:",
            parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup([[b("❌ Cancel","cancel_action")]]))
        return

    if data == "nb_number_list":
        rows = db_get_countries()
        if not rows:
            await query.edit_message_text("📦 Stock is empty.",
                reply_markup=InlineKeyboardMarkup([[b("🔙 Back","menu_numbers")]]))
            return
        await query.edit_message_text("📋 <b>STOCK</b> - Tap to delete:",
            parse_mode="HTML", reply_markup=get_nb_stock_keyboard())
        return

    if data == "nb_delete_menu":
        rows = db_get_countries()
        if not rows:
            await query.answer("No stock", show_alert=True)
            return
        await query.edit_message_text("🗑️ <b>SELECT COUNTRY TO DELETE:</b>",
            parse_mode="HTML", reply_markup=get_nb_stock_keyboard())
        return

    if data.startswith("nb_del|"):
        country = data.split("|", 1)[1]
        db_delete_country(country)
        await query.edit_message_text(f"✅ <b>{country}</b> deleted.", parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup([[b("🔙 Back","menu_numbers")]]))
        return

    if data == "nb_stock_stats":
        rows  = db_get_countries()
        total = db_total_numbers()
        lines = "\n".join([f"  {c}: {n}" for c,n in rows]) or "  Empty"
        await query.edit_message_text(
            f"📊 <b>STOCK STATS</b>\n━━━━━━━━━━━━━━━━━━━━━━\nTotal: <b>{total}</b>\n\n{lines}",
            parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup([[b("🔙 Back","menu_numbers")]]))
        return

    if data == "nb_export":
        rows = db_get_countries()
        if not rows:
            await query.answer("No numbers to export", show_alert=True)
            return
        lines = []
        for country, _ in rows:
            nums = db_get_country_numbers(country)
            lines.append(f"=== {country} ===")
            lines.extend(nums)
        fname = f"numbers_export_{int(time.time())}.txt"
        with open(fname, "w") as f:
            f.write("\n".join(lines))
        async with Bot(token=BOT_TOKEN) as bot_inst:
            await bot_inst.send_document(chat_id=query.message.chat_id,
                document=open(fname, "rb"),
                caption=f"📤 Numbers Export — {db_total_numbers()} total")
        os.remove(fname)
        await query.edit_message_text("✅ Numbers exported.",
            reply_markup=InlineKeyboardMarkup([[b("🔙 Back","menu_numbers")]]))
        return

    # ══ FILE MANAGER ══════════════════════════════════════════
    if data == "menu_files":
        if not has_perm(uid,"files"): await query.answer("❌ No permission.",show_alert=True); return
        flist = []
        for f in [LOG_FILE, OTP_FILE, DB_FILE, PANEL_FILE, IVAS_FILE,
                  CONFIG_FILE, ADMINS_FILE, GROUP_FILE]:
            if os.path.exists(f):
                flist.append(f"{f} — {os.path.getsize(f):,}b")
        await query.edit_message_text(
            f"📂 <b>FILE MANAGER</b>\n━━━━━━━━━━━━━━━━━━━━━━\n<code>"
            + "\n".join(flist) + "</code>",
            parse_mode="HTML", reply_markup=get_files_menu())
        return

    if data == "fm_list":
        flist = []
        for f in [LOG_FILE, OTP_FILE, DB_FILE, PANEL_FILE, IVAS_FILE,
                  CONFIG_FILE, ADMINS_FILE, GROUP_FILE]:
            if os.path.exists(f):
                flist.append(f"{f} ({os.path.getsize(f):,}b)")
        await query.edit_message_text(
            "📂 <b>FILES:</b>\n<code>" + "\n".join(flist) + "</code>",
            parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup([[b("🔙 Back","menu_files")]]))
        return

    for file_data, file_path, caption in [
        ("fm_download_log", LOG_FILE, "📋 Bot Log"),
        ("fm_download_otp", OTP_FILE, "🗄 OTP Store"),
        ("fm_download_db",  DB_FILE,  "🗄 SQLite DB"),
    ]:
        if data == file_data:
            if not os.path.exists(file_path):
                await query.answer("File not found", show_alert=True)
                return
            async with Bot(token=BOT_TOKEN) as bot_inst:
                await bot_inst.send_document(chat_id=query.message.chat_id,
                    document=open(file_path, "rb"), caption=caption)
            await query.answer("✅ Sent", show_alert=True)
            return

    if data == "fm_clear_log":
        await query.edit_message_text("🗑️ Clear the bot log file?",
            reply_markup=get_confirmation_keyboard("clear_log"))
        return

    if data == "confirm_clear_log":
        open(LOG_FILE, "w").close()
        await query.edit_message_text("✅ Log cleared.",
            reply_markup=InlineKeyboardMarkup([[b("🔙 Back","menu_files")]]))
        return

    # ══ PANEL MANAGER ═════════════════════════════════════════
    if data == "menu_panels":
        if not has_perm(uid,"panels"): await query.answer("❌ No permission.",show_alert=True); return
        await query.edit_message_text(
            "📡 <b>PANEL MANAGER</b>\n━━━━━━━━━━━━━━━━━━━━━━\nSelect option:",
            parse_mode="HTML", reply_markup=get_panels_menu())
        return

    if data == "list_panels":
        panels = load_panels()
        text   = "📋 <b>REST PANELS</b>\n━━━━━━━━━━━━━━━━━━━━━━\n"
        for name, pd in panels.items():
            active = (name in REST_TASKS and not REST_TASKS[name].done())
            hits   = STATS["panel_hits"].get(name, 0)
            st     = "🟢" if active else "🔴"
            atype  = pd.get("api_type", "unknown")
            tbadge = {"old": "🔵", "mo": "🟣", "ps": "🟢"}.get(atype, "🔍")
            text  += f"\n{st} <b>{name}</b> {tbadge}\n   {pd['url'][:50]}\n   Hits: {hits}\n"
        await query.edit_message_text(text or "No panels.", parse_mode="HTML",
            reply_markup=get_panels_keyboard("view"))
        return

    if data == "add_panel":
        PANEL_ADD_STATES[uid] = {"step":"name","data":{},"timestamp":time.time()}
        await query.edit_message_text(
            "➕ <b>ADD REST PANEL</b>\n━━━━━━━━━━━━━━━━━━━━━━\n"
            "Bot supports <b>3 API types</b> — all auto-detected:\n\n"
            "🔵 <b>Old API</b> — viewstats panels\n"
            "🟣 <b>MO API</b> — MOAPI reseller/mdr.php\n"
            "🟢 <b>PS API</b> — pscall.net smsreport\n\n"
            "Just enter the URL + token and the bot detects the type automatically!\n\n"
            "━━━━━━━━━━━━━━━━━━━━━━\n"
            "📛 <b>Step 1: Panel Name</b>\nSend a name for this panel:",
            parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup([[b("❌ Cancel","cancel_action")]]))
        return

    if data == "remove_panel":
        await query.edit_message_text("🗑️ <b>SELECT PANEL TO REMOVE:</b>",
            parse_mode="HTML", reply_markup=get_panels_keyboard("remove"))
        return

    if data.startswith("view_panel_"):
        panel  = data.replace("view_panel_", "")
        panels = load_panels()
        if panel not in panels:
            await query.answer("Not found", show_alert=True)
            return
        pd     = panels[panel]
        active = (panel in REST_TASKS and not REST_TASKS[panel].done())
        atype  = pd.get("api_type", "unknown")
        tbadge = {"old": "🔵 Old API", "mo": "🟣 MO API", "ps": "🟢 PS API"}.get(atype, "🔍 Auto-detect")
        tklabel = "Key" if atype == "ps" else "Token"
        await query.edit_message_text(
            f"{'🟢' if active else '🔴'} <b>{panel.upper()}</b>\n━━━━━━━━━━━━━━━━━━━━━━\n"
            f"🤖 Type:    {tbadge}\n"
            f"🔗 URL:     <code>{pd['url']}</code>\n"
            f"🔑 {tklabel}: <code>{pd['token'][:30]}...</code>\n"
            f"📊 Records: <code>{pd.get('records',20)}</code>\n"
            f"📈 Hits:    <code>{STATS['panel_hits'].get(panel,0)}</code>",
            parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup([
                [b("🔄 Re-detect API Type", f"redetect_panel_{panel}")],
                [b("🔙 Back","list_panels")]
            ]))
        return

    if data.startswith("remove_panel_"):
        panel = data.replace("remove_panel_", "")
        await query.edit_message_text(f"🟡 Remove panel <b>{panel}</b>?", parse_mode="HTML",
            reply_markup=get_confirmation_keyboard("remove_panel", panel))
        return

    if data.startswith("confirm_remove_panel_"):
        panel  = data.replace("confirm_remove_panel_", "")
        panels = load_panels()
        if panel in panels:
            del panels[panel]
            save_panels(panels)
            API_PANELS = panels
        if panel in REST_TASKS:
            REST_TASKS[panel].cancel()
            del REST_TASKS[panel]
        await query.edit_message_text(f"✅ Panel <b>{panel}</b> removed.", parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup([[b("🔙 Back","menu_panels")]]))
        return

    if data.startswith("redetect_panel_"):
        panel  = data.replace("redetect_panel_", "")
        panels = load_panels()
        if panel not in panels:
            await query.answer("Panel not found", show_alert=True)
            return
        # Force re-detection by clearing cached type
        panels[panel]["api_type"] = "unknown"
        API_PANELS[panel]["api_type"] = "unknown"
        await query.answer("🔍 Detecting...", show_alert=False)
        detected = _detect_api_type(API_PANELS[panel])
        panels[panel]["api_type"] = detected
        save_panels(panels)
        tbadge = {"old": "🔵 Old API", "mo": "🟣 MO API", "ps": "🟢 PS API"}.get(detected, "🔍 Unknown")
        await query.answer(f"Detected: {tbadge}", show_alert=True)
        # Re-open the panel view
        active = (panel in REST_TASKS and not REST_TASKS[panel].done())
        pd     = panels[panel]
        tklabel = "Key" if detected == "ps" else "Token"
        await query.edit_message_text(
            f"{'🟢' if active else '🔴'} <b>{panel.upper()}</b>\n━━━━━━━━━━━━━━━━━━━━━━\n"
            f"🤖 Type:    {tbadge}\n"
            f"🔗 URL:     <code>{pd['url']}</code>\n"
            f"🔑 {tklabel}: <code>{pd['token'][:30]}...</code>\n"
            f"📊 Records: <code>{pd.get('records',20)}</code>\n"
            f"📈 Hits:    <code>{STATS['panel_hits'].get(panel,0)}</code>",
            parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup([
                [b("🔄 Re-detect API Type", f"redetect_panel_{panel}")],
                [b("🔙 Back","list_panels")]
            ]))
        return

    if data == "confirm_add_panel":
        if uid not in PANEL_ADD_STATES or PANEL_ADD_STATES[uid]["step"] != "confirm":
            await query.edit_message_text("❌ No pending panel.")
            return
        pd = PANEL_ADD_STATES[uid]["data"]
        # Always store base URL + token separately — _fetch_ps_api combines them safely
        clean_url   = pd["url"].split("?")[0].rstrip("/")
        clean_token = pd["token"].strip()
        API_PANELS[pd["name"]] = {
            "url":      clean_url,
            "token":    clean_token,
            "records":  pd.get("records", 20),
            "api_type": pd.get("api_type", "unknown")
        }
        save_panels(API_PANELS)
        task = asyncio.create_task(api_worker(pd["name"]), name=f"REST-{pd['name']}")
        task.add_done_callback(handle_task_exception)
        REST_TASKS[pd["name"]] = task
        del PANEL_ADD_STATES[uid]
        type_badge = {"old": "🔵 Old API", "mo": "🟣 MO API", "ps": "🟢 PS API"}.get(pd.get("api_type",""), "🔍 Auto")
        await query.edit_message_text(
            f"✅ <b>Panel Added & Started!</b>\n━━━━━━━━━━━━━━━━━━━━━━\n"
            f"📛 Name: <b>{pd['name']}</b>\n"
            f"🤖 Type: {type_badge}\n"
            f"🔗 URL:  <code>{clean_url}</code>\n"
            f"🟢 Worker is running!",
            parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup([[b("📋 View Panels","list_panels")],[b("🔙 Back","menu_panels")]]))
        return

    if data == "panel_fetch_all":
        wait    = await context.bot.send_message(chat_id=query.message.chat_id, text="🔄 Fetching...")
        results = fetch_all_panels(limit=3)
        if not results:
            await wait.edit_text("❌ Nothing fetched.")
            return
        text = f"📨 <b>FETCHED {len(results)}</b>\n━━━━━━━━━━━━━━━━━━━━━━\n"
        for r in results[:8]:
            otp  = extract_otp(r["message"]) or "N/A"
            text += (f"📡 <b>{r['panel']}</b> | {r['service']}\n"
                     f"📞 <code>{r['number']}</code>  🔑 <code>{otp}</code>\n"
                     f"💬 {r['message'][:60]}\n──────────────────────\n")
        await wait.edit_text(text[:4000], parse_mode="HTML")
        return

    # ══ IVAS MANAGER ══════════════════════════════════════════
    if data == "menu_ivas":
        if not has_perm(uid,"ivas"): await query.answer("❌ No permission.",show_alert=True); return
        await query.edit_message_text(
            "🔌 <b>IVAS MANAGER</b>\n━━━━━━━━━━━━━━━━━━━━━━\nSelect option:",
            parse_mode="HTML", reply_markup=get_ivas_menu())
        return

    if data == "list_ivas":
        accounts = load_ivas()
        if not accounts:
            await query.edit_message_text("🟡 No IVAS accounts yet.",
                parse_mode="HTML",
                reply_markup=InlineKeyboardMarkup([
                    [b("➕ Add IVAS","add_ivas")],
                    [b("🔙 Back","menu_ivas")]]))
            return
        text = "🔌 <b>IVAS ACCOUNTS</b>\n━━━━━━━━━━━━━━━━━━━━━━\n"
        for name in accounts:
            active = (name in IVAS_TASKS and not IVAS_TASKS[name].done())
            hits   = STATS["ivas_hits"].get(name, 0)
            st     = "🟢" if active else "🔴"
            text  += f"\n{st} <b>{name}</b> (hits:{hits})\n"
        await query.edit_message_text(text, parse_mode="HTML",
            reply_markup=get_ivas_keyboard("view"))
        return

    if data == "add_ivas":
        IVAS_ADD_STATES[uid] = {"step":"name","data":{},"timestamp":time.time()}
        await query.edit_message_text(
            "🔌 <b>ADD IVAS</b>\n━━━━━━━━━━━━━━━━━━━━━━\nStep 1: Account name:",
            parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup([[b("❌ Cancel","cancel_action")]]))
        return

    if data == "remove_ivas":
        await query.edit_message_text("🗑️ <b>SELECT IVAS TO REMOVE:</b>",
            parse_mode="HTML", reply_markup=get_ivas_keyboard("remove"))
        return

    if data == "ivas_restart_all":
        for name in list(IVAS_TASKS.keys()):
            IVAS_TASKS[name].cancel()
            del IVAS_TASKS[name]
        for name in load_ivas():
            task = asyncio.create_task(ivas_worker(name), name=f"IVAS-{name}")
            task.add_done_callback(handle_task_exception)
            IVAS_TASKS[name] = task
        await query.edit_message_text("✅ All IVAS workers restarted.",
            reply_markup=InlineKeyboardMarkup([[b("🔙 Back","menu_ivas")]]))
        return

    if data.startswith("view_ivas_"):
        name     = data.replace("view_ivas_", "")
        accounts = load_ivas()
        if name not in accounts:
            await query.answer("Not found", show_alert=True)
            return
        active = (name in IVAS_TASKS and not IVAS_TASKS[name].done())
        hits   = STATS["ivas_hits"].get(name, 0)
        uri    = accounts[name].get("uri", "N/A")
        await query.edit_message_text(
            f"{'🟢' if active else '🔴'} <b>IVAS: {name.upper()}</b>\n━━━━━━━━━━━━━━━━━━━━━━\n"
            f"Status: {'Running' if active else 'Stopped'}\n"
            f"Hits: <code>{hits}</code>\n"
            f"URI: <code>{uri[:80]}...</code>",
            parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup([[b("🔙 Back","list_ivas")]]))
        return

    if data.startswith("remove_ivas_"):
        name = data.replace("remove_ivas_", "")
        await query.edit_message_text(f"🟡 Remove IVAS <b>{name}</b>?", parse_mode="HTML",
            reply_markup=get_confirmation_keyboard("remove_ivas", name))
        return

    if data.startswith("confirm_remove_ivas_"):
        name     = data.replace("confirm_remove_ivas_", "")
        accounts = load_ivas()
        if name in accounts:
            del accounts[name]
            save_ivas(accounts)
        if name in IVAS_TASKS:
            IVAS_TASKS[name].cancel()
            del IVAS_TASKS[name]
        await query.edit_message_text(f"✅ IVAS <b>{name}</b> removed.", parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup([[b("🔙 Back","menu_ivas")]]))
        return

    if data == "confirm_add_ivas":
        if uid not in IVAS_ADD_STATES or IVAS_ADD_STATES[uid]["step"] != "confirm":
            await query.edit_message_text("❌ No pending IVAS.")
            return
        pd       = IVAS_ADD_STATES[uid]["data"]
        accounts = load_ivas()
        accounts[pd["name"]] = {"uri": pd["uri"]}
        save_ivas(accounts)
        task = asyncio.create_task(ivas_worker(pd["name"]), name=f"IVAS-{pd['name']}")
        task.add_done_callback(handle_task_exception)
        IVAS_TASKS[pd["name"]] = task
        del IVAS_ADD_STATES[uid]
        await query.edit_message_text(f"✅ IVAS <b>{pd['name']}</b> added!",
            parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup([[b("🔙 Back","menu_ivas")]]))
        return

    # ══ FETCH SMS ══════════════════════════════════════════════
    if data == "menu_fetch":
        if not has_perm(uid,"fetch_sms"): await query.answer("❌ No permission.",show_alert=True); return
        await query.edit_message_text(
            "🔄 <b>FETCH SMS</b>\n━━━━━━━━━━━━━━━━━━━━━━\nSelect method:",
            parse_mode="HTML", reply_markup=get_fetch_menu())
        return

    if data == "fetch_all_now":
        wait    = await context.bot.send_message(chat_id=query.message.chat_id, text="🔄 Fetching...")
        results = fetch_all_panels(limit=5)
        if not results:
            await wait.edit_text("❌ Nothing fetched.")
            return
        text = f"📨 <b>LATEST SMS ({len(results)})</b>\n━━━━━━━━━━━━━━━━━━━━━━\n"
        for r in results[:10]:
            otp  = extract_otp(r["message"]) or "N/A"
            text += (f"📡 <b>{r['panel']}</b> | {r['service']}\n"
                     f"📞 <code>{r['number']}</code>\n"
                     f"🔑 OTP: <code>{otp}</code>\n"
                     f"💬 {r['message'][:80]}\n──────────────────────\n")
        await wait.edit_text(text[:4000], parse_mode="HTML")
        return

    if data == "fetch_by_number":
        FETCH_STATES[uid] = {"step":"waiting_number","timestamp":time.time()}
        await query.edit_message_text(
            "🔍 <b>FETCH BY NUMBER</b>\n━━━━━━━━━━━━━━━━━━━━━━\nSend the phone number:",
            parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup([[b("❌ Cancel","cancel_action")]]))
        return

    if data == "fetch_single_panel":
        panels = load_panels()
        kb     = [[b(name.upper(), f"fetch_panel_{name}")] for name in panels]
        kb.append([b("🔙 Back","menu_fetch")])
        await query.edit_message_text("📡 <b>SELECT PANEL:</b>",
            parse_mode="HTML", reply_markup=InlineKeyboardMarkup(kb))
        return

    if data.startswith("fetch_panel_"):
        panel  = data.replace("fetch_panel_", "")
        result = fetch_latest(panel)
        if result:
            otp = extract_otp(result["message"]) or "N/A"
            await query.edit_message_text(
                f"📡 <b>Panel: {panel}</b>\n━━━━━━━━━━━━━━━━━━━━━━\n"
                f"📞 <code>{result['number']}</code>\n"
                f"🔑 OTP: <code>{otp}</code>\n"
                f"📱 Service: {result['service']}\n"
                f"💬 {result['message'][:200]}\n"
                f"⏱ {result['time']}",
                parse_mode="HTML",
                reply_markup=InlineKeyboardMarkup([[b("🔙 Back","menu_fetch")]]))
        else:
            await query.edit_message_text(f"❌ No data from <b>{panel}</b>.", parse_mode="HTML",
                reply_markup=InlineKeyboardMarkup([[b("🔙 Back","menu_fetch")]]))
        return

    # ══ OTP HISTORY ═══════════════════════════════════════════
    if data == "menu_otp_history":
        if not has_perm(uid,"otp_history"): await query.answer("❌ No permission.",show_alert=True); return
        last    = db_get_otp_history(5)
        preview = "".join([f"📞 <code>{r[0]}</code> 🔑 <code>{r[2]}</code> {r[3]}\n"
                           for r in last]) or "No history yet"
        await query.edit_message_text(
            f"📋 <b>OTP HISTORY</b>\n━━━━━━━━━━━━━━━━━━━━━━\n{preview}",
            parse_mode="HTML", reply_markup=get_otp_history_menu())
        return

    if data in ("otp_hist_10","otp_hist_20"):
        limit = 10 if data == "otp_hist_10" else 20
        rows  = db_get_otp_history(limit)
        if not rows:
            await query.answer("No history", show_alert=True)
            return
        text = f"📋 <b>LAST {limit} OTPs</b>\n━━━━━━━━━━━━━━━━━━━━━━\n"
        for row in rows:
            text += (f"📞 <code>{row[0]}</code> | <b>{row[1]}</b>\n"
                     f"🔑 <code>{row[2]}</code> | {row[3]} | {row[4]}\n──────────\n")
        await query.edit_message_text(text[:4000], parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup([[b("🔙 Back","menu_otp_history")]]))
        return

    if data == "otp_export_hist":
        rows = db_get_otp_history(9999)
        if not rows:
            await query.answer("No history", show_alert=True)
            return
        fname = f"otp_history_{int(time.time())}.csv"
        with open(fname, "w") as f:
            f.write("number,service,otp,source,time\n")
            for row in rows:
                f.write(",".join(str(x) for x in row) + "\n")
        async with Bot(token=BOT_TOKEN) as bot_inst:
            await bot_inst.send_document(chat_id=query.message.chat_id,
                document=open(fname,"rb"),
                caption=f"📤 OTP History — {len(rows)} records")
        os.remove(fname)
        await query.answer("✅ Exported", show_alert=True)
        return

    if data == "otp_search_num":
        FETCH_STATES[uid] = {"step":"waiting_number","timestamp":time.time()}
        await query.edit_message_text(
            "🔍 <b>SEARCH OTP BY NUMBER</b>\n━━━━━━━━━━━━━━━━━━━━━━\nSend the number:",
            parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup([[b("❌ Cancel","cancel_action")]]))
        return

    if data == "otp_clear_hist":
        await query.edit_message_text("🗑️ Clear ALL OTP history?",
            reply_markup=get_confirmation_keyboard("otp_clear_hist"))
        return

    if data == "confirm_otp_clear_hist":
        db_clear_otp_history()
        await query.edit_message_text("✅ History cleared.",
            reply_markup=InlineKeyboardMarkup([[b("🔙 Back","menu_otp_history")]]))
        return

    # ══ GROUP MANAGER ═════════════════════════════════════════
    if data == "menu_groups":
        if not has_perm(uid,"groups"): await query.answer("❌ No permission.",show_alert=True); return
        groups = load_groups()
        config = load_config()
        lg     = config.get("log_group") or "Not set"
        await query.edit_message_text(
            f"👥 <b>GROUP MANAGER</b>\n━━━━━━━━━━━━━━━━━━━━━━\n"
            f"OTP Groups: <b>{len(groups)}</b>\n"
            f"Log Group: <code>{lg}</code>",
            parse_mode="HTML", reply_markup=get_groups_menu())
        return

    if data == "add_group_prompt":
        SETTING_STATES[uid] = {"step":"waiting_group_id","timestamp":time.time()}
        await query.edit_message_text(
            "➕ <b>ADD OTP GROUP</b>\n━━━━━━━━━━━━━━━━━━━━━━\nSend the group chat ID:",
            parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup([[b("❌ Cancel","cancel_action")]]))
        return

    if data.startswith("del_group_"):
        try:
            gid    = int(data.replace("del_group_", ""))
            groups = load_groups()
            if gid in groups:
                groups.remove(gid)
                save_groups(groups)
            await query.edit_message_text(f"✅ Group <code>{gid}</code> removed.", parse_mode="HTML",
                reply_markup=InlineKeyboardMarkup([[b("🔙 Back","menu_groups")]]))
        except:
            await query.answer("Error", show_alert=True)
        return

    if data in ("set_log_group","set_log_group_settings"):
        SETTING_STATES[uid] = {"step":"waiting_log_group","timestamp":time.time()}
        await query.edit_message_text(
            "📋 <b>SET LOG GROUP</b>\n━━━━━━━━━━━━━━━━━━━━━━\nSend log group chat ID:",
            parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup([[b("❌ Cancel","cancel_action")]]))
        return

    if data == "clear_log_group":
        config = load_config()
        config["log_group"] = None
        save_config(config)
        await query.edit_message_text("✅ Log group cleared.",
            reply_markup=InlineKeyboardMarkup([[b("🔙 Back","menu_groups")]]))
        return

    # ══ STATS / STATUS ════════════════════════════════════════
    if data == "stats":
        if not has_perm(uid,"stats"): await query.answer("❌ No permission.",show_alert=True); return
        total, active_today, active_week = db_user_stats()
        uptime = str(datetime.now() - datetime.fromtimestamp(STATS['start_time'])).split('.')[0]
        await query.edit_message_text(
            f"📊 <b>BOT STATS</b>\n━━━━━━━━━━━━━━━━━━━━━━\n"
            f"⏱ Uptime: <code>{uptime}</code>\n"
            f"👤 Users: <code>{total}</code> | Today: <code>{active_today}</code>\n"
            f"📊 OTPs Sent: <code>{STATS['otps_sent']}</code>\n"
            f"🚫 Dropped: <code>{STATS['otps_dropped']}</code>\n"
            f"❌ Errors: <code>{STATS['errors']}</code>\n"
            f"📦 Numbers: <code>{db_total_numbers()}</code>\n"
            f"🗄 OTP Store: <code>{len(load_otp_store())}</code>\n"
            f"━━━━━━━━━━━━━━━━━━━━━━", parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup([[b("🔙 Back","back_to_admin")]]))
        return

    if data == "status":
        if not has_perm(uid,"stats"): await query.answer("❌ No permission.",show_alert=True); return
        await query.edit_message_text(_build_status(), parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup([[b("🔙 Back","back_to_admin")]]))
        return

    # ══ BROADCAST ═════════════════════════════════════════════
    if data == "broadcast":
        if not has_perm(uid,"broadcast"): await query.answer("❌ No permission.",show_alert=True); return
        await query.edit_message_text("📢 <b>BROADCAST</b>\n━━━━━━━━━━━━━━━━━━━━━━\nChoose type:",
            parse_mode="HTML", reply_markup=get_broadcast_keyboard())
        return

    if data == "broadcast_text":
        BROADCAST_STATES[uid] = {"type":"text","step":"waiting_message","timestamp":time.time()}
        await query.edit_message_text("📢 Send your broadcast message:",
            reply_markup=InlineKeyboardMarkup([[b("❌ Cancel","cancel_action")]]))
        return

    if data == "broadcast_with_buttons":
        BROADCAST_STATES[uid] = {"type":"with_buttons","step":"waiting_message","timestamp":time.time()}
        await query.edit_message_text(
            "📢 Send text + buttons.\nFormat:\nYour message\n[Button Label|https://url]",
            reply_markup=InlineKeyboardMarkup([[b("❌ Cancel","cancel_action")]]))
        return

    if data == "confirm_broadcast":
        if uid not in BROADCAST_STATES or BROADCAST_STATES[uid]["step"] != "confirm":
            await query.edit_message_text("❌ No pending broadcast.")
            return
        msg_text = BROADCAST_STATES[uid]["message"]
        del BROADCAST_STATES[uid]
        await query.edit_message_text("📢 Broadcasting to all users...")
        stats = await do_broadcast(context.bot, msg_text)
        await query.edit_message_text(
            f"📢 <b>BROADCAST COMPLETE</b>\n"
            f"━━━━━━━━━━━━━━━━━━━━━━\n"
            f"👥 Total: <code>{stats['total']}</code>\n"
            f"✅ Success: <code>{stats['success']}</code>\n"
            f"❌ Failed: <code>{stats['fail']}</code>",
            parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup([[b("🔙 Back","back_to_admin")]]))
        return

    if data == "confirm_broadcast_buttons":
        if uid not in BROADCAST_STATES or BROADCAST_STATES[uid]["step"] != "confirm":
            await query.edit_message_text("❌ No pending broadcast.")
            return
        state   = BROADCAST_STATES[uid]
        buttons = state.get("buttons", [])
        kb      = InlineKeyboardMarkup([[btn_] for btn_ in buttons]) if buttons else None
        msg_text = state["message"]
        del BROADCAST_STATES[uid]
        await query.edit_message_text("📢 Broadcasting to all users...")
        stats = await do_broadcast(context.bot, msg_text, kb)
        await query.edit_message_text(
            f"📢 <b>BROADCAST COMPLETE</b>\n"
            f"━━━━━━━━━━━━━━━━━━━━━━\n"
            f"👥 Total Users: <code>{stats['total']}</code>\n"
            f"✅ Success: <code>{stats['success']}</code>\n"
            f"❌ Failed: <code>{stats['fail']}</code>",
            parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup([[b("🔙 Back","back_to_admin")]]))
        return

    # ══ SETTINGS ══════════════════════════════════════════════
    if data == "menu_settings":
        if not has_perm(uid,"settings"): await query.answer("❌ No permission.",show_alert=True); return
        await query.edit_message_text(
            "⚙️ <b>SETTINGS</b>\n━━━━━━━━━━━━━━━━━━━━━━\nSelect option:",
            parse_mode="HTML", reply_markup=get_settings_menu())
        return

    if data == "toggle_otp_forward":
        config = load_config()
        config["otp_forward"] = not config.get("otp_forward", True)
        save_config(config)
        st = "✅ ENABLED" if config["otp_forward"] else "❌ DISABLED"
        await query.edit_message_text(f"📤 OTP Forwarding: <b>{st}</b>", parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup([[b("🔙 Back","menu_settings")]]))
        return

    if data in ("set_forward_delay","set_channel","set_numberbot",
                "set_otp_group_link","set_log_group"):
        step_map = {
            "set_forward_delay": ("waiting_delay",    "⏱ SET FORWARD DELAY\nSend seconds (0-60):"),
            "set_channel":       ("waiting_channel",  "📢 SET CHANNEL LINK\nSend the URL:"),
            "set_numberbot":     ("waiting_numberbot","🤖 SET NUMBER BOT LINK\nSend the URL:"),
            "set_otp_group_link":("waiting_otp_link", "🔗 SET OTP GROUP LINK\nSend the URL:"),
            "set_log_group":     ("waiting_log_group","📋 SET LOG GROUP\nSend the chat ID:"),
        }
        step, prompt = step_map[data]
        SETTING_STATES[uid] = {"step": step, "timestamp": time.time()}
        await query.edit_message_text(
            f"⚙️ <b>{prompt}</b>", parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup([[b("❌ Cancel","cancel_action")]]))
        return

    if data == "menu_admin_manager":
        if not is_owner(uid):
            await query.answer("❌ Owner only!", show_alert=True)
            return
        staff = load_staff()
        await query.edit_message_text(
            f"👤 <b>STAFF MANAGER</b>\n━━━━━━━━━━━━━━━━━━━━━━\n"
            f"👑 Owners: <b>{len(OWNER_IDS)}</b>\n"
            f"🛡️ Staff Members: <b>{len(staff)}</b>\n\n"
            f"Tap a staff member to edit their permissions.\n"
            f"Each permission can be toggled ON/OFF individually.",
            parse_mode="HTML", reply_markup=get_admin_manager_keyboard())
        return

    if data == "add_staff_prompt":
        if not is_owner(uid):
            await query.answer("❌ Owner only!", show_alert=True)
            return
        SETTING_STATES[uid] = {"step": "waiting_staff_id", "timestamp": time.time()}
        await query.edit_message_text(
            "➕ <b>ADD STAFF MEMBER</b>\n━━━━━━━━━━━━━━━━━━━━━━\n"
            "Send the Telegram <b>User ID</b> of the new staff member:",
            parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup([[b("❌ Cancel", "cancel_action")]]))
        return

    if data.startswith("edit_staff_"):
        if not is_owner(uid):
            await query.answer("❌ Owner only!", show_alert=True)
            return
        target_str = data.replace("edit_staff_", "")
        staff      = load_staff()
        info       = staff.get(target_str, {})
        name       = info.get("name", target_str)
        perms      = info.get("perms", [])
        perm_lines = "\n".join([
            f"  {'✅' if p in perms else '☑️'} {ALL_PERMISSIONS[p]}"
            for p in ALL_PERMISSIONS
        ])
        await query.edit_message_text(
            f"🛡️ <b>EDIT PERMISSIONS</b>\n"
            f"━━━━━━━━━━━━━━━━━━━━━━\n"
            f"User: <code>{target_str}</code> ({name})\n"
            f"Active Perms: <b>{len(perms)}/{len(ALL_PERMISSIONS)}</b>\n\n"
            f"{perm_lines}",
            parse_mode="HTML",
            reply_markup=get_staff_perms_keyboard(target_str))
        return

    if data.startswith("toggle_perm_"):
        if not is_owner(uid):
            await query.answer("❌ Owner only!", show_alert=True)
            return
        rest       = data.replace("toggle_perm_", "", 1)
        perm_key   = None
        target_str = None
        for pk in ALL_PERMISSIONS:
            if rest.endswith("_" + pk):
                perm_key   = pk
                target_str = rest[:-(len(pk)+1)]
                break
        if not perm_key or not target_str:
            await query.answer("Error parsing perm", show_alert=True)
            return
        staff = load_staff()
        if target_str not in staff:
            await query.answer("Staff not found", show_alert=True)
            return
        perms = staff[target_str].get("perms", [])
        if perm_key in perms:
            perms.remove(perm_key)
            action = "Removed"
        else:
            perms.append(perm_key)
            action = "Added"
        staff[target_str]["perms"] = perms
        save_staff(staff)
        await query.answer(f"{action}: {ALL_PERMISSIONS[perm_key]}", show_alert=False)
        info       = staff[target_str]
        name       = info.get("name", target_str)
        perm_lines = "\n".join([
            f"  {'✅' if p in perms else '☑️'} {ALL_PERMISSIONS[p]}"
            for p in ALL_PERMISSIONS
        ])
        await query.edit_message_text(
            f"🛡️ <b>EDIT PERMISSIONS</b>\n"
            f"━━━━━━━━━━━━━━━━━━━━━━\n"
            f"User: <code>{target_str}</code> ({name})\n"
            f"Active Perms: <b>{len(perms)}/{len(ALL_PERMISSIONS)}</b>\n\n"
            f"{perm_lines}",
            parse_mode="HTML",
            reply_markup=get_staff_perms_keyboard(target_str))
        return

    if data.startswith("grant_all_"):
        if not is_owner(uid):
            await query.answer("❌ Owner only!", show_alert=True)
            return
        target_str = data.replace("grant_all_", "")
        staff      = load_staff()
        if target_str in staff:
            staff[target_str]["perms"] = list(ALL_PERMISSIONS.keys())
            save_staff(staff)
        await query.answer("✅ All permissions granted", show_alert=True)
        await query.edit_message_text(
            f"✅ All permissions granted to <code>{target_str}</code>.",
            parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup([[b("🔙 Back", "menu_admin_manager")]]))
        return

    if data.startswith("revoke_all_"):
        if not is_owner(uid):
            await query.answer("❌ Owner only!", show_alert=True)
            return
        target_str = data.replace("revoke_all_", "")
        staff      = load_staff()
        if target_str in staff:
            staff[target_str]["perms"] = []
            save_staff(staff)
        await query.answer("❌ All permissions revoked", show_alert=True)
        await query.edit_message_text(
            f"❌ All permissions revoked from <code>{target_str}</code>.",
            parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup([[b("🔙 Back", "menu_admin_manager")]]))
        return

    if data.startswith("remove_staff_"):
        if not is_owner(uid):
            await query.answer("❌ Owner only!", show_alert=True)
            return
        target_str = data.replace("remove_staff_", "")
        try:
            target_int = int(target_str)
            if target_int in OWNER_IDS:
                await query.answer("❌ Cannot remove owner!", show_alert=True)
                return
            remove_staff(target_int)
            await query.edit_message_text(
                f"✅ Staff member <code>{target_str}</code> removed.",
                parse_mode="HTML",
                reply_markup=InlineKeyboardMarkup([[b("🔙 Back", "menu_admin_manager")]]))
        except:
            await query.answer("Error", show_alert=True)
        return

    # ══ ADVANCED ══════════════════════════════════════════════
    if data == "menu_advanced":
        if not has_perm(uid,"advanced"): await query.answer("❌ No permission.",show_alert=True); return
        await query.edit_message_text(
            "🔧 <b>ADVANCED TOOLS</b>\n━━━━━━━━━━━━━━━━━━━━━━\nSelect option:",
            parse_mode="HTML", reply_markup=get_advanced_keyboard())
        return

    if data == "restart_workers":
        await _restart_all_workers()
        await query.edit_message_text("✅ All workers restarted.",
            reply_markup=InlineKeyboardMarkup([[b("🔙 Back","menu_advanced")]]))
        return

    if data == "restart_bot":
        if not is_owner(uid):
            await query.answer("❌ Owner only!", show_alert=True)
            return
        await query.edit_message_text("🔁 Restarting bot...")
        await asyncio.sleep(1)
        os.execv(sys.executable, [sys.executable] + sys.argv)
        return

    if data in ("stop_forward","start_forward"):
        config = load_config()
        config["otp_forward"] = (data == "start_forward")
        save_config(config)
        st = "✅ ENABLED" if config["otp_forward"] else "❌ DISABLED"
        await query.edit_message_text(f"📤 OTP Forwarding: <b>{st}</b>", parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup([[b("🔙 Back","menu_advanced")]]))
        return

    if data == "reload_config":
        API_PANELS = load_panels()
        await query.edit_message_text("✅ Config reloaded from all JSON files.",
            reply_markup=InlineKeyboardMarkup([[b("🔙 Back","menu_advanced")]]))
        return

    if data == "clear_all_otps":
        await query.edit_message_text("🗑️ Delete ALL stored OTPs?",
            reply_markup=get_confirmation_keyboard("clear_all_otps"))
        return

    if data == "confirm_clear_all_otps":
        save_otp_store({})
        await query.edit_message_text("✅ OTP store cleared.",
            reply_markup=InlineKeyboardMarkup([[b("🔙 Back","menu_advanced")]]))
        return

    if data == "export_otps":
        store = load_otp_store()
        if not store:
            await query.answer("No OTPs to export", show_alert=True)
            return
        fname = f"otp_export_{int(time.time())}.json"
        with open(fname, "w") as f:
            json.dump(store, f, indent=4)
        async with Bot(token=BOT_TOKEN) as bot_inst:
            await bot_inst.send_document(chat_id=query.message.chat_id,
                document=open(fname,"rb"),
                caption=f"📤 OTP Store — {len(store)} entries")
        os.remove(fname)
        await query.answer("✅ Exported", show_alert=True)
        return

    if data == "view_logs":
        try:
            with open(LOG_FILE, "r") as f:
                lines = f.readlines()[-25:]
            log_text = "".join(lines)
            if len(log_text) > 3500:
                log_text = log_text[-3500:]
            await query.edit_message_text(
                f"<b>Last 25 log lines:</b>\n<pre>{log_text}</pre>",
                parse_mode="HTML",
                reply_markup=InlineKeyboardMarkup([[b("🔙 Back","menu_advanced")]]))
        except Exception as e:
            await query.edit_message_text(f"Error reading logs: {e}")
        return

    if data in ("test_panels_menu","test_panels_adv"):
        panels = load_panels()
        if not panels:
            await query.edit_message_text("No panels configured.")
            return
        results = []
        for name in panels:
            try:
                d2 = fetch_latest(name)
                results.append(f"{'✅' if d2 else '❌'} {name}: {'Online' if d2 else 'Offline'}")
            except Exception as e:
                results.append(f"❌ {name}: {e}")
        await query.edit_message_text(
            "🧪 <b>Panel Test Results</b>\n━━━━━━━━━━━━━━━━━━━━━━\n" + "\n".join(results),
            parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup([[b("🔙 Back","menu_advanced")]]))
        return

    if data == "worker_status":
        lines = []
        for p in load_panels():
            alive = (p in REST_TASKS and not REST_TASKS[p].done())
            lines.append(f"{'🟢' if alive else '🔴'} REST: {p} (hits:{STATS['panel_hits'].get(p,0)})")
        for n in load_ivas():
            alive = (n in IVAS_TASKS and not IVAS_TASKS[n].done())
            lines.append(f"{'🟢' if alive else '🔴'} IVAS: {n} (hits:{STATS['ivas_hits'].get(n,0)})")
        await query.edit_message_text(
            "📊 <b>WORKER STATUS</b>\n━━━━━━━━━━━━━━━━━━━━━━\n" + "\n".join(lines or ["No workers"]),
            parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup([[b("🔙 Back","menu_advanced")]]))
        return

    if data == "confirm_clear_otps":
        save_otp_store({})
        await query.edit_message_text("✅ OTP store cleared.",
            reply_markup=InlineKeyboardMarkup([[b("🔙 Back","back_to_admin")]]))
        return

    if data == "cancel_action":
        for d in [PANEL_ADD_STATES, IVAS_ADD_STATES, BROADCAST_STATES,
                  SETTING_STATES, FETCH_STATES, NB_STATE]:
            d.pop(uid, None)
        await query.edit_message_text("❌ Action cancelled.",
            reply_markup=InlineKeyboardMarkup([[b("🔙 Back","back_to_admin")]]))
        return

# ═══════════════════════════════════════════════════════════════
#  MESSAGE HANDLER
# ═══════════════════════════════════════════════════════════════
async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid  = update.effective_user.id
    text = update.message.text or ""

    if text == "/cancel":
        for d in [PANEL_ADD_STATES, IVAS_ADD_STATES, BROADCAST_STATES,
                  SETTING_STATES, FETCH_STATES, NB_STATE]:
            d.pop(uid, None)
        await update.message.reply_text("❌ Cancelled.")
        return

    # ── Number add flow ───────────────────────────────────────
    if uid in NB_STATE:
        state = NB_STATE[uid]
        if isinstance(state, dict) and state.get("step") == "waiting_country":
            NB_STATE[uid] = {"step":"waiting_file","country":text,"timestamp":time.time()}
            await update.message.reply_text(
                f"📄 Now send a <b>.txt file</b> (one number per line) for <b>{text}</b>:",
                parse_mode="HTML")
        return

    # ── Settings wizard ───────────────────────────────────────
    if uid in SETTING_STATES:
        state = SETTING_STATES[uid]
        state["timestamp"] = time.time()
        step  = state.get("step")

        if step == "waiting_group_id":
            try:
                gid = int(text.strip())
                groups = load_groups()
                if gid not in groups:
                    groups.append(gid)
                    save_groups(groups)
                    await update.message.reply_text(f"✅ Group <code>{gid}</code> added.", parse_mode="HTML")
                else:
                    await update.message.reply_text("🟡 Already exists.")
            except:
                await update.message.reply_text("❌ Invalid chat ID.")
            del SETTING_STATES[uid]

        elif step == "waiting_log_group":
            try:
                gid = int(text.strip())
                config = load_config()
                config["log_group"] = gid
                save_config(config)
                await update.message.reply_text(f"✅ Log group set to <code>{gid}</code>.", parse_mode="HTML")
            except:
                await update.message.reply_text("❌ Invalid chat ID.")
            del SETTING_STATES[uid]

        elif step == "waiting_delay":
            try:
                delay = int(text.strip())
                if not 0 <= delay <= 60:
                    raise ValueError
                config = load_config()
                config["forward_delay"] = delay
                save_config(config)
                await update.message.reply_text(f"✅ Forward delay set to <b>{delay}s</b>.", parse_mode="HTML")
            except:
                await update.message.reply_text("❌ Enter a number 0-60.")
            del SETTING_STATES[uid]

        elif step == "waiting_channel":
            config = load_config()
            config["channel_link"] = text.strip()
            save_config(config)
            await update.message.reply_text("✅ Channel link updated.")
            del SETTING_STATES[uid]

        elif step == "waiting_numberbot":
            config = load_config()
            config["number_bot_link"] = text.strip()
            save_config(config)
            await update.message.reply_text("✅ Number bot link updated.")
            del SETTING_STATES[uid]

        elif step == "waiting_otp_link":
            config = load_config()
            config["channel_link"] = text.strip()
            save_config(config)
            await update.message.reply_text("✅ OTP group link updated.")
            del SETTING_STATES[uid]

        elif step == "waiting_staff_id":
            if not is_owner(uid):
                await update.message.reply_text("❌ Owner only!")
                del SETTING_STATES[uid]
                return
            try:
                new_uid = int(text.strip())
                if new_uid in OWNER_IDS:
                    await update.message.reply_text("🟡 That user is already an owner.")
                    del SETTING_STATES[uid]
                    return
                staff = load_staff()
                if str(new_uid) in staff:
                    await update.message.reply_text("🟡 Already a staff member. Use edit to change permissions.")
                    del SETTING_STATES[uid]
                    return
                add_staff(new_uid, str(new_uid), [])
                await update.message.reply_text(
                    f"✅ Staff member <code>{new_uid}</code> added with no permissions.\n\n"
                    f"Now go to Staff Manager and tap their name to assign permissions.",
                    parse_mode="HTML",
                    reply_markup=InlineKeyboardMarkup([[b("👤 Open Staff Manager", "menu_admin_manager")]]))
            except ValueError:
                await update.message.reply_text("❌ Invalid user ID. Send a numeric Telegram user ID.")
            del SETTING_STATES[uid]
        return

    # ── Fetch by number ───────────────────────────────────────
    if uid in FETCH_STATES:
        state = FETCH_STATES[uid]
        state["timestamp"] = time.time()
        if state.get("step") == "waiting_number":
            target = text.strip().replace("+", "")
            found  = None
            store  = load_otp_store()
            for k, v in store.items():
                if target in k:
                    found = v
                    break
            if not found:
                rows = db_search_otp_by_number(target)
                if rows:
                    found = rows[0][2]
            if not found:
                for panel in API_PANELS:
                    d2 = fetch_latest(panel)
                    if d2 and target in d2["number"]:
                        found = extract_otp(d2["message"])
                        break
            if found:
                await update.message.reply_text(
                    f"✅ <b>OTP FOUND</b>\n📞 <code>{target}</code>\n🔑 <code>{found}</code>",
                    parse_mode="HTML")
            else:
                await update.message.reply_text(
                    f"❌ No OTP found for <code>{target}</code>", parse_mode="HTML")
            del FETCH_STATES[uid]
        return

    # ── Panel add wizard ──────────────────────────────────────
    if uid in PANEL_ADD_STATES:
        state = PANEL_ADD_STATES[uid]
        state["timestamp"] = time.time()
        if state["step"] == "name":
            state["data"]["name"] = text
            state["step"] = "url"
            await update.message.reply_text(
                "📡 <b>Step 2: API URL</b>\n"
                "Send the full API URL.\n\n"
                "<b>Examples:</b>\n"
                "• Old API: <code>http://147.135.212.197/crapi/had/viewstats</code>\n"
                "• MO API:  <code>http://137.74.1.203/crapi/reseller/mdr.php</code>\n"
                "• PS API:  <code>https://pscall.net/restapi/smsreport</code>",
                parse_mode="HTML")
        elif state["step"] == "url":
            if not text.startswith("http"):
                await update.message.reply_text("❌ Must start with http:// or https://")
                return
            state["data"]["url"] = text
            state["data"]["api_type"] = "unknown"   # will be auto-detected
            state["step"] = "token"
            await update.message.reply_text(
                "🔑 <b>Step 3: Token / Key</b>\n"
                "Send the API token or key.\n\n"
                "• For Old API and MO API — send the <b>token</b>\n"
                "• For PS API — send the <b>key</b>\n"
                "  (e.g. <code>YOUR_PS_API_TOKEN_HERE</code>)",
                parse_mode="HTML")
        elif state["step"] == "token":
            state["data"]["token"] = text
            state["step"] = "records"
            await update.message.reply_text("📊 <b>Step 4:</b> Records count to fetch (1-200):")
        elif state["step"] == "records":
            try:
                rec = int(text)
                if not 1 <= rec <= 200:
                    raise ValueError
            except:
                await update.message.reply_text("❌ Enter a number between 1-200:")
                return
            state["data"]["records"] = rec
            state["step"] = "confirm"
            # Auto-detect API type for preview
            probe_cfg = {
                "url":   state["data"]["url"],
                "token": state["data"]["token"]
            }
            detected = _detect_api_type(probe_cfg)
            state["data"]["api_type"] = detected
            type_badge = {"old": "🔵 Old API", "mo": "🟣 MO API", "ps": "🟢 PS API"}.get(detected, "🔍 Auto-detect")
            await update.message.reply_text(
                f"➕ <b>CONFIRM ADD PANEL</b>\n━━━━━━━━━━━━━━━━━━━━━━\n"
                f"📛 Name:    <code>{state['data']['name']}</code>\n"
                f"🔗 URL:     <code>{state['data']['url']}</code>\n"
                f"🔑 Token:   <code>{state['data']['token'][:30]}...</code>\n"
                f"📊 Records: <code>{rec}</code>\n"
                f"🤖 Type:    {type_badge}\n"
                f"━━━━━━━━━━━━━━━━━━━━━━\nConfirm?",
                parse_mode="HTML", reply_markup=get_confirmation_keyboard("add_panel"))
        return

    # ── IVAS add wizard ───────────────────────────────────────
    if uid in IVAS_ADD_STATES:
        state = IVAS_ADD_STATES[uid]
        state["timestamp"] = time.time()
        if state["step"] == "name":
            state["data"]["name"] = text
            state["step"] = "uri"
            await update.message.reply_text(
                "Step 2: IVAS WebSocket URI (<code>wss://...</code>):", parse_mode="HTML")
        elif state["step"] == "uri":
            if not text.startswith("wss://"):
                await update.message.reply_text("❌ Must start with <code>wss://</code>", parse_mode="HTML")
                return
            state["data"]["uri"] = text
            state["step"] = "confirm"
            await update.message.reply_text(
                f"🔌 <b>CONFIRM ADD IVAS</b>\n━━━━━━━━━━━━━━━━━━━━━━\n"
                f"Name: <code>{state['data']['name']}</code>\n"
                f"URI: <code>{state['data']['uri'][:80]}...</code>\n━━━━━━━━━━━━━━━━━━━━━━\nConfirm?",
                parse_mode="HTML", reply_markup=get_confirmation_keyboard("add_ivas"))
        return

    # ── Broadcast wizard ──────────────────────────────────────
    if uid in BROADCAST_STATES:
        state = BROADCAST_STATES[uid]
        state["timestamp"] = time.time()
        if state["step"] == "waiting_message":
            if state["type"] == "text":
                state["message"] = text
                state["step"]    = "confirm"
                await update.message.reply_text(
                    f"Preview:\n{text[:200]}{'...' if len(text)>200 else ''}\n\nSend?",
                    reply_markup=get_confirmation_keyboard("broadcast"))
            elif state["type"] == "with_buttons":
                lines    = text.split('\n')
                msg_text = ""
                buttons  = []
                for line in lines:
                    if line.startswith('[') and line.endswith(']') and '|' in line:
                        parts = line[1:-1].split('|', 1)
                        buttons.append(InlineKeyboardButton(parts[0].strip(), url=parts[1].strip()))
                    else:
                        msg_text += line + '\n'
                state["message"] = msg_text.strip()
                state["buttons"] = buttons
                state["step"]    = "confirm"
                await update.message.reply_text(
                    f"Preview with {len(buttons)} button(s). Send?",
                    reply_markup=get_confirmation_keyboard("broadcast_buttons"))
        return

# ═══════════════════════════════════════════════════════════════
#  DOCUMENT HANDLER
# ═══════════════════════════════════════════════════════════════
async def document_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    if uid not in NB_STATE or not isinstance(NB_STATE[uid], dict):
        return
    state = NB_STATE[uid]
    if state.get("step") != "waiting_file":
        return
    country = state["country"]
    try:
        file       = await update.message.document.get_file()
        file_bytes = await file.download_as_bytearray()
        file_text  = file_bytes.decode("utf-8")
        all_lines  = [n.strip() for n in file_text.splitlines() if n.strip()]
        nums       = [n for n in all_lines if n.isdigit()] or all_lines
        db_add_numbers(country, nums)
        await update.message.reply_text(
            f"✅ <b>{len(nums)}</b> numbers added to <b>{country}</b>!",
            parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup([[b("🔙 Back to Admin","back_to_admin")]]))
        del NB_STATE[uid]
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {e}")

# ═══════════════════════════════════════════════════════════════
#  MAIN
# ═══════════════════════════════════════════════════════════════
async def main():
    logger.info(f"🚀 {BOT_NAME} starting...")
    logger.info(f"📡 OTP Groups: {load_groups()}")
    logger.info(f"🔌 IVAS accounts: {list(load_ivas().keys())}")
    logger.info(f"📋 REST panels: {list(API_PANELS.keys())}")
    logger.info(f"⚙️  OTP forward: {load_config().get('otp_forward', True)}")

    asyncio.create_task(cleanup_states())
    asyncio.create_task(monitor_tasks())
    asyncio.create_task(_otp_sender_task())

    for panel in API_PANELS:
        task = asyncio.create_task(api_worker(panel), name=f"REST-{panel}")
        task.add_done_callback(handle_task_exception)
        REST_TASKS[panel] = task

    for name in load_ivas():
        task = asyncio.create_task(ivas_worker(name), name=f"IVAS-{name}")
        task.add_done_callback(handle_task_exception)
        IVAS_TASKS[name] = task

    app = Application.builder().token(BOT_TOKEN).build()

    for cmd, handler in [
        ("start",       start_command),
        ("help",        help_command),
        ("admin",       admin_command),
        ("otpfor",      otpfor_command),
        ("fetchsms",    fetchsms_command),
        ("status",      status_command),
        ("stats",       stats_command),
        ("broadcast",   broadcast_command),
        ("addgroup",    addgroup_command),
        ("removegroup", removegroup_command),
        ("reload",      reload_command),
    ]:
        app.add_handler(CommandHandler(cmd, handler))

    app.add_handler(CallbackQueryHandler(callback_query_handler))
    app.add_handler(MessageHandler(filters.Document.ALL, document_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))

    await app.initialize()
    await app.start()
    await app.updater.start_polling(drop_pending_updates=True)
    logger.info("🟢 Bot is online.")
    try:
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        logger.info("Bot stopped.")
        await app.stop()

if __name__ == "__main__":
    asyncio.run(main())







