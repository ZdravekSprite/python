# ============================================
# DEVICE DASHBOARD – Teltonika API
# ============================================

from flask import Flask, render_template, jsonify
import threading
import time
import sqlite3
import requests
import json
from datetime import datetime, timezone
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
from threading import Lock
import sys, os

# ============================================
# CONFIG
# ============================================

root_folder = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(root_folder)

from config import FOTA_API_TOKEN as API_TOKEN
from email_cfg import smtp_host, smtp_port, smtp_user, smtp_pass, email_to, email_from

DB_FILE = "devices.db"
sync_lock = Lock()

API_BASE = "https://api.teltonika.lt"
PER_PAGE = 100

# ============================================
# DATABASE
# ============================================

class Database:
    def __init__(self, path):
        self.conn = sqlite3.connect(path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self.c = self.conn.cursor()
        self._setup()

    def _setup(self):
        self.c.execute("""
        CREATE TABLE IF NOT EXISTS devices (
            imei TEXT PRIMARY KEY,
            model TEXT,
            activity_status TEXT,
            description TEXT,
            updated_at TEXT,
            raw_json TEXT,
            current_firmware TEXT
        )
        """)
        self.conn.commit()
    '''
    def _setup(self):
        self.c.execute("""
        CREATE TABLE IF NOT EXISTS devices (
            imei TEXT PRIMARY KEY,
            model TEXT,
            activity_status TEXT,
            description TEXT,
            updated_at TEXT,
            raw_json TEXT
        )
        """)
        self.conn.commit()
    '''

    def get_device(self, imei):
        self.c.execute("SELECT * FROM devices WHERE imei = ?", (imei,))
        return self.c.fetchone()

    def upsert_device(self, dev):
        normalized_json = json.dumps(dev, sort_keys=True)
        self.c.execute("""
        INSERT OR REPLACE INTO devices (
            imei, model, activity_status, description,
            updated_at, raw_json, current_firmware
        ) VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            dev["imei"],
            dev.get("model"),
            dev.get("activity_status"),
            dev.get("description"),
            datetime.now(timezone.utc).isoformat(),
            normalized_json,
            dev.get("current_firmware")  # <-- novi stupac
        ))
        self.conn.commit()
    '''
    def upsert_device(self, dev):
        normalized_json = json.dumps(dev, sort_keys=True)
        self.c.execute("""
        INSERT OR REPLACE INTO devices (
            imei, model, activity_status, description,
            updated_at, raw_json
        ) VALUES (?, ?, ?, ?, ?, ?)
        """, (
            dev["imei"],
            dev.get("model"),
            dev.get("activity_status"),
            dev.get("description"),
            datetime.now(timezone.utc).isoformat(),
            normalized_json
        ))
        self.conn.commit()
    '''

def get_db():
    return Database(DB_FILE)


# ============================================
# EMAIL SENDER
# ============================================

def send_email(subject, body):
    msg = MIMEMultipart()
    msg["From"] = email_from
    msg["To"] = email_to
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP(smtp_host, smtp_port) as server:
            server.starttls()
            server.login(smtp_user, smtp_pass)
            server.sendmail(email_from, email_to, msg.as_string())
        print(f"📧 Email poslan: {subject}")
    except Exception as e:
        print(f"❌ Email error: {e}")


# ============================================
# API HELPERS
# ============================================

def api_get(url, params=None):
    headers = {"Authorization": f"Bearer {API_TOKEN}"}
    r = requests.get(url, headers=headers, params=params, timeout=15)

    if r.status_code == 429:
        time.sleep(5)
        return api_get(url, params)

    r.raise_for_status()
    return r.json()


def get_device_list(page):
    return api_get(f"{API_BASE}/devices", params={
        "page": page,
        "per_page": PER_PAGE,
        "order": "asc"
    })


def get_device_details(imei):
    return api_get(f"{API_BASE}/devices/{imei}")


# ============================================
# SYNC STATUS STORAGE
# ============================================

sync_status = {
    "running": False,
    "current_page": 0,
    "total_pages": 1,
    "last_sync": None,
    "next_sync": None
}


# ============================================
# SYNC LOGIC
# ============================================

def sync_all_devices():
    if not sync_lock.acquire(blocking=False):
        print("⚠ Sync već u tijeku!")
        return

    print("🔄 Pokrećem sync uređaja...")
    db = get_db()
    sync_status["running"] = True
    sync_status["current_page"] = 1

    page = 1

    while True:
        try:
            r = get_device_list(page)
            devices = r.get("data", [])
            last_page = r.get("last_page", page)
            sync_status["total_pages"] = last_page
        except Exception as e:
            print(f"❌ Greška dohvaćanja stranice {page}: {e}")
            break

        if not devices:
            break

        sync_status["current_page"] = page

        for dev in devices:
            imei = str(dev.get("imei"))
            if not imei:
                continue

            try:
                details = get_device_details(imei)
            except Exception as e:
                print(f"❌ Detalji greška za {imei}: {e}")
                continue

            merged = details
            merged["current_firmware"] = details.get("current_firmware")  # <-- ovo dodajemo
            existing = db.get_device(imei)
            new_raw = json.dumps(merged, sort_keys=True)
            old_raw = existing["raw_json"] if existing else None

            if existing is None:
                print(f"➕ Novi uređaj: {imei}")
                db.upsert_device(merged)

            elif new_raw != old_raw:
                print(f"🔄 Ažuriram uređaj: {imei}")
                db.upsert_device(merged)
                #send_email(f"Device update: {imei}", json.dumps(merged, indent=2))

            else:
                print(f"✔ Uređaj {imei} aktualan", end="\r")

            time.sleep(0.1)

        if page >= last_page:
            break

        page += 1

    sync_status["running"] = False
    sync_status["last_sync"] = datetime.now(timezone.utc).isoformat()
    sync_status["next_sync"] = int(time.time()) + 1800
    sync_lock.release()

    print("✅ Sync završen.")


# ============================================
# FLASK APP
# ============================================

app = Flask(__name__)


def query_db(query, params=()):
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute(query, params)
    rows = c.fetchall()
    conn.close()
    return rows


# --------------------------------------------
# ROUTES
# --------------------------------------------

@app.route("/")
def index():
    return render_template("devices.html")


@app.route("/api/devices")
def api_devices():
    rows = query_db("SELECT * FROM devices ORDER BY updated_at DESC")
    return jsonify([dict(r) for r in rows])


@app.route("/api/status-stats")
def api_status_stats():
    rows = query_db("""
        SELECT activity_status, COUNT(*) AS count
        FROM devices GROUP BY activity_status
    """)
    return jsonify({
        "labels": [row["activity_status"] or "Unknown" for row in rows],
        "counts": [row["count"] for row in rows]
    })


@app.route("/api/update-trend")
def api_update_trend():
    rows = query_db("""
        SELECT substr(updated_at,1,10) AS day, COUNT(*) as count
        FROM devices
        GROUP BY day ORDER BY day ASC
    """)
    return jsonify({
        "labels": [row["day"] for row in rows],
        "counts": [row["count"] for row in rows]
    })


@app.route("/api/model-stats")
def api_model_stats():
    rows = query_db("""
        SELECT model, COUNT(*) AS count
        FROM devices
        GROUP BY model
    """)
    return jsonify({
        "labels": [row["model"] or "Unknown" for row in rows],
        "counts": [row["count"] for row in rows]
    })


@app.route("/api/sync-status")
def api_sync():
    return jsonify(sync_status)

@app.route("/api/models")
def api_models():
    # Dohvati sve modele iz baze
    rows = query_db("SELECT DISTINCT model FROM devices WHERE model IS NOT NULL ORDER BY model ASC")
    models = [row["model"] for row in rows]
    return jsonify(models)
# ============================================
# BACKGROUND SYNC THREAD
# ============================================

def background_loader():
    while True:
        try:
            now = int(time.time())
            if not sync_status["running"] and now >= (sync_status["next_sync"] or 0):
                sync_all_devices()
        except Exception as e:
            print("❌ Background sync greška:", e)

        time.sleep(60)


# ============================================
# START
# ============================================

if __name__ == "__main__":
    #db = get_db()
    #db.c.execute("ALTER TABLE devices ADD COLUMN current_firmware TEXT")
    #db.conn.commit()
    t = threading.Thread(target=background_loader, daemon=True)
    t.start()
    print("📊 Dashboard dostupno na http://localhost:5000")
    app.run(host="0.0.0.0", port=5000, debug=True)
