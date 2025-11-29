import sys, os
from threading import Lock
import sqlite3
import json
from datetime import datetime, timezone
import time
import requests
import threading

# ============================================
# CONFIG
# ============================================

root_folder = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(root_folder)

from config import FOTA_API_TOKEN as TELTONIKA_API_TOKEN
from config import token as TRUPHONE_API_TOKEN

TELTONIKA_API_BASE = "https://api.teltonika.lt"
TRUPHONE_API_BASE = "https://iot.truphone.com/api/v2.2"

PER_PAGE = 100

DB_FILE = "data.db"
sync_lock = Lock()

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
            current_firmware TEXT,
            updated_at TEXT,
            raw_json TEXT
        )
        """)
        self.c.execute("""
        CREATE TABLE IF NOT EXISTS sims (
            iccid TEXT PRIMARY KEY,
            msisdn_primary TEXT,
            status TEXT,
            label TEXT,
            description TEXT,
            updated_at TEXT,
            raw_json TEXT
        )
        """)
        self.conn.commit()

    def get_device(self, imei):
        self.c.execute("SELECT * FROM devices WHERE imei = ?", (imei,))
        return self.c.fetchone()

    def upsert_device(self, dev):
        normalized_json = json.dumps(dev, sort_keys=True)
        self.c.execute("""
        INSERT OR REPLACE INTO devices (
            imei, model, activity_status, description, current_firmware,
            updated_at, raw_json
        ) VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            dev["imei"],
            dev.get("model"),
            dev.get("activity_status"),
            dev.get("description"),
            dev.get("current_firmware"),
            datetime.now(timezone.utc).isoformat(),
            normalized_json
        ))
        self.conn.commit()

    def get_sim(self, iccid):
        self.c.execute("SELECT * FROM sims WHERE iccid = ?", (iccid,))
        return self.c.fetchone()

    def upsert_sim(self, sim):
        normalized_json = json.dumps(sim, sort_keys=True)
        self.c.execute("""
        INSERT OR REPLACE INTO sims (
            iccid, msisdn_primary, status, label, description,
            updated_at, raw_json
        ) VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            sim["iccid"],
            sim.get("primaryMsisdn"),
            sim.get("status"),
            sim.get("label"),
            sim.get("description"),
            datetime.now(timezone.utc).isoformat(),
            normalized_json
        ))
        self.conn.commit()

def get_db():
    return Database(DB_FILE)

def query_db(query, params=()):
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute(query, params)
    rows = c.fetchall()
    conn.close()
    return rows

# ============================================
# API HELPERS
# ============================================

def api_get(url, params=None, api="teltonika"):
    if api == "teltonika":
        headers = {"Authorization": f"Bearer {TELTONIKA_API_TOKEN}"}
    elif api == "truphone":
        headers = {"Authorization": f"Token {TRUPHONE_API_TOKEN}"}
    else:
        raise ValueError("Unknown API type")
    
    r = requests.get(url, headers=headers, params=params, timeout=15)

    if r.status_code == 429:
        time.sleep(5)
        return api_get(url, params)

    r.raise_for_status()
    return r.json()


def get_dev_list(page):
    return api_get(f"{TELTONIKA_API_BASE}/devices", params={
        "page": page,
        "per_page": PER_PAGE,
        "order": "asc"
    })

def get_sim_list(page):
    return api_get(f"{TRUPHONE_API_BASE}/sims/", params={
        "page": page,
        "per_page": PER_PAGE
    }, api='truphone')

def get_dev_details(imei):
    return api_get(f"{TELTONIKA_API_BASE}/devices/{imei}")

def get_sim_details(iccid):
    return api_get(f"{TRUPHONE_API_BASE}/sims/{iccid}", api='truphone')

def get_sim_status(iccid):
    return api_get(f"{TRUPHONE_API_BASE}/sims/{iccid}/status", api='truphone')

# ============================================
# SYNC STATUS STORAGE
# ============================================

sync_status = {
    "dev_running": False,
    "dev_current_page": 0,
    "dev_total_pages": 1,
    "dev_last_sync": None,
    "dev_next_sync": None,
    "sim_running": False,
    "sim_current_page": 0,
    "sim_total_pages": 1,
    "sim_last_sync": None,
    "sim_next_sync": None,
}

# ===============================
# SYNC LOGIKA
# ===============================

def sync_all_devices():
    if not sync_lock.acquire(blocking=False):
        print("\033[K ⚠ Sync već u tijeku!")
        return

    print("\033[K 🔄 Pokrećem sync uređaja...")
    db = get_db()
    sync_status["dev_running"] = True
    sync_status["dev_current_page"] = 1

    page = 1

    while True:
        try:
            r = get_dev_list(page)
            devices = r.get("data", [])
            last_page = r.get("last_page", page)
            sync_status["dev_total_pages"] = last_page
        except Exception as e:
            print(f"\033[K ❌ Greška dohvaćanja stranice {page}: {e}")
            break

        if not devices:
            break

        sync_status["dev_current_page"] = page

        for dev in devices:
            imei = str(dev.get("imei"))
            if not imei:
                continue

            try:
                details = get_dev_details(imei)
            except Exception as e:
                print(f"\033[K ❌ Detalji greška za {imei}: {e}")
                continue

            merged = details
            merged["current_firmware"] = details.get("current_firmware")  # <-- ovo dodajemo
            existing = db.get_device(imei)
            new_raw = json.dumps(merged, sort_keys=True)
            old_raw = existing["raw_json"] if existing else None

            if existing is None:
                print(f"\033[K ➕ Novi uređaj: {imei}")
                db.upsert_device(merged)

            elif new_raw != old_raw:
                print(f"\033[K 🔄 Ažuriram uređaj: {imei}")
                db.upsert_device(merged)
            else:
                print(f"\033[K ✔ Uređaj {imei} aktualan", end="\r")

            time.sleep(0.1)

        if page >= last_page:
            break

        page += 1

    sync_status["dev_running"] = False
    sync_status["dev_last_sync"] = datetime.now(timezone.utc).isoformat()
    sync_status["dev_next_sync"] = int(time.time()) + 3600  # sljedeći sync za 60 min
    sync_lock.release()
    print("\033[K ✅ Sync uređaja završen.")
    rows = query_db("SELECT * FROM devices")
    print(f"\033[K ✅ U bazi {len(rows)} uređaja.")

def sync_all_sims():
    if not sync_lock.acquire(blocking=False):
        print("\033[K ⚠ Sync već u tijeku! Preskačem...")
        return

    print("\033[K 🔄 Počinje SIM sync...")
    db = get_db()
    sync_status["sim_running"] = True
    sync_status["sim_current_page"] = 0
    sync_status["sim_total_pages"] = 0

    page = 1

    while True:
        try:
            r = get_sim_list(page)
            sims = r or []
            if sync_status["sim_total_pages"] < page:
                sync_status["sim_total_pages"] = page
        except Exception as e:
            print(f"\033[K ❌ Greška dohvaćanja stranice {page}: {e}")
            break

        if not sims:
            break

        sync_status["sim_current_page"] = page

        for sim in sims:
            iccid = sim.get("iccid")
            if not iccid:
                continue

            try:
                details = get_sim_details(iccid)
                status = get_sim_status(iccid)
            except Exception as e:
                print(f"\033[K ❌ Greška dohvaćanja podataka za {iccid}: {e}")
                continue

            merged = {**details, "status": json.dumps(status.get("status"), sort_keys=True)}

            existing = db.get_sim(iccid)
            new_raw = json.dumps(merged, sort_keys=True)
            old_raw = existing["raw_json"] if existing else None

            if existing is None:
                print(f"\033[K ➕ Novi SIM: {iccid}")
                db.upsert_sim(merged)
            elif new_raw != old_raw:
                print(f"\033[K 🔄 Ažuriram SIM: {iccid}")
                db.upsert_sim(merged)

            else:
                print(f"\033[K ✔ SIM {iccid} već aktualan", end="\r")

            time.sleep(0.15)

        if len(sims) < PER_PAGE:
            break
        page += 1

    sync_status["sim_running"] = False
    sync_status["sim_last_sync"] = datetime.now(timezone.utc).isoformat()
    sync_status["sim_next_sync"] = int(time.time()) + 3600  # sljedeći sync za 60 min
    print("\033[K ✅ SIM Sync gotov.")
    sync_lock.release()
    rows = query_db("SELECT * FROM sims")
    print(f"\033[K ✅ U bazi {len(rows)} SIM.")

# ============================================
# BACKGROUND SYNC THREAD
# ============================================

def background_loader():
    while True:
        try:
            now_ts = int(time.time())
            next_dev_ts = sync_status.get("dev_next_sync") or 0
            if not sync_status["dev_running"] and now_ts >= next_dev_ts:
                sync_all_devices()
            now_ts = int(time.time())
            next_sim_ts = sync_status.get("sim_next_sync") or 0
            if not sync_status["sim_running"] and now_ts >= next_sim_ts:
                sync_all_sims()
        except Exception as e:
            print("\033[K ❌ Background sync greška:", e)

        time.sleep(60)

from flask import Flask, render_template, jsonify
app = Flask(__name__)

# ===============================
# ROUTES
# ===============================
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/sync-status")
def api_sync_status():
    return jsonify(sync_status)

# ============================================
# START
# ============================================

if __name__ == "__main__":
    t = threading.Thread(target=background_loader, daemon=True)
    t.start()
    #r = get_dev_list(1)
    #r = get_sim_list(1)
    #print(r)
    print("📊 Dashboard dostupan na http://localhost:5000")
    app.run(host="0.0.0.0", port=5000, debug=True)



