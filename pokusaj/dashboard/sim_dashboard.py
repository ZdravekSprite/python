#dashboard
from flask import Flask, render_template, jsonify
import threading
import time
import sqlite3

import requests
import sqlite3
import time
import json
from datetime import datetime, timezone
from email_cfg import smtp_host, smtp_port, smtp_user, smtp_pass, email_to, email_from
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from threading import Lock

import sys
import os
# Get the root folder dynamically
root_folder = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(root_folder)
# Now you can import your module
from config import token as API_TOKEN

# ===============================
# DATABASE
# ===============================
DB_FILE = "sims.db"
sync_lock = Lock()   # sprječava paralelni sync

class Database:
    def __init__(self, path):
        self.conn = sqlite3.connect(path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self.c = self.conn.cursor()
        self._setup()

    def _setup(self):
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

    def get_sim(self, iccid):
        self.c.execute("SELECT * FROM sims WHERE iccid = ?", (iccid,))
        return self.c.fetchone()

    def upsert_sim(self, sim_data):
        normalized_json = json.dumps(sim_data, sort_keys=True)
        self.c.execute("""
        INSERT OR REPLACE INTO sims (
            iccid, msisdn_primary, status, label, description,
            updated_at, raw_json
        ) VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            sim_data["iccid"],
            sim_data.get("primaryMsisdn"),
            sim_data.get("status"),
            sim_data.get("label"),
            sim_data.get("description"),
            datetime.now(timezone.utc).isoformat(),
            normalized_json
        ))
        self.conn.commit()


def get_db():
    """Svaki thread dobiva vlastitu SQLite konekciju."""
    return Database(DB_FILE)


# ===============================
# EMAIL
# ===============================
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
        print(f"❌ Email slanje neuspješno: {e}")


# ===============================
# API
# ===============================
API_BASE_V20 = "https://iot.truphone.com/api/v2.0"
API_BASE_V22 = "https://iot.truphone.com/api/v2.2"
PER_PAGE = 100

def api_get(url, params=None):
    headers = {"Authorization": f"Token {API_TOKEN}", "Accept": "application/json"}
    r = requests.get(url, headers=headers, params=params, timeout=30)
    if r.status_code == 429:
        time.sleep(5)
        return api_get(url, params)
    r.raise_for_status()
    return r.json()

def get_sim_list(page):
    return api_get(f"{API_BASE_V20}/sims/", params={"page": page, "per_page": PER_PAGE})

def get_sim_details(iccid):
    return api_get(f"{API_BASE_V22}/sims/{iccid}")

def get_sim_status(iccid):
    return api_get(f"{API_BASE_V20}/sims/{iccid}/status")


# ===============================
# SYNC STATUS
# ===============================
sync_status = {
    "running": False,
    "current_page": 0,
    "total_pages": 37,
    "last_sync": None,
    "next_sync": None
}


# ===============================
# SYNC LOGIKA
# ===============================
def extract_sim_list_response(data):
    if isinstance(data, dict) and "results" in data:
        return data["results"]
    elif isinstance(data, list):
        return data
    else:
        return []


def sync_all_sims():
    """
    Sync svih SIM kartica koristeći paginaciju preko page parametra.
    Prvo učitava prvu stranicu da odredi ukupni broj stranica.
    """
    if not sync_lock.acquire(blocking=False):
        print("⚠ Sync već u tijeku! Preskačem...")
        return

    print("🔄 Počinje sync svih SIM kartica...")
    db = get_db()
    sync_status["running"] = True
    sync_status["current_page"] = 0
    #sync_status["total_pages"] = 0

    page = 1

    # ===============================
    # Iteriraj sve stranice
    # ===============================
    while True: #page <= total_pages:
        sync_status["current_page"] = page

        # Ako nije prva stranica, učitaj je
        #if page != 1:
        try:
            r = get_sim_list(page)
            sims = extract_sim_list_response(r)
        except Exception as e:
            print(f"❌ Greška dohvaćanja stranice {page}: {e}")
            break

        if not sims:
            break

        if page > sync_status["total_pages"]:
            sync_status["total_pages"] = page

        for sim in sims:
            iccid = sim.get("iccid")
            if not iccid:
                continue

            try:
                details = get_sim_details(iccid)
                status = get_sim_status(iccid)
            except Exception as e:
                print(f"❌ Greška dohvaćanja podataka za {iccid}: {e}")
                continue

            merged = {**details, "status": status.get("status")}

            existing = db.get_sim(iccid)
            new_raw = json.dumps(merged, sort_keys=True)
            old_raw = existing["raw_json"] if existing else None

            if existing is None:
                print(f"➕ Novi SIM: {iccid}")
                db.upsert_sim(merged)
            elif new_raw != old_raw:
                print(f"🔄 Ažuriram SIM: {iccid}")
                db.upsert_sim(merged)

                # email notifikacija
                subject = f"SIM promjena: {iccid}"
                body = f"""Detektirana je promjena na SIM kartici:
ICCID: {iccid}
Label: {merged.get('label')}
Status: {merged.get('status')}
Vrijeme: {datetime.now(timezone.utc).isoformat()}

JSON podaci:
{json.dumps(merged, indent=2)}
"""
                send_email(subject, body)
            else:
                print(f"✔ SIM {iccid} već aktualan", end="\r")

            time.sleep(0.15)

        page += 1

    # ===============================
    # Sync završen
    # ===============================
    sync_status["running"] = False
    sync_status["last_sync"] = datetime.now(timezone.utc).isoformat()
    sync_status["next_sync"] = int(time.time()) + 1800  # sljedeći sync za 30 min
    print("✅ Sync gotov.")
    sync_lock.release()


DB_FILE = "sims.db"
app = Flask(__name__)

# ===============================
# DATABASE HELPERS
# ===============================
def query_db(query, params=()):
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute(query, params)
    rows = c.fetchall()
    conn.close()
    return rows

# ===============================
# ROUTES
# ===============================
@app.route("/")
def index():
    return render_template("sims.html")

@app.route("/api/sims")
def api_sims():
    sims = query_db("SELECT * FROM sims ORDER BY updated_at DESC")
    sims = [dict(row) for row in sims]
    return jsonify(sims)

@app.route("/api/status-stats")
def api_status_stats():
    rows = query_db("""
        SELECT status, COUNT(*) AS count
        FROM sims
        GROUP BY status
    """)
    return jsonify({
        "labels": [row["status"] for row in rows],
        "counts": [row["count"] for row in rows]
    })

@app.route("/api/update-trend")
def api_update_trend():
    rows = query_db("""
        SELECT substr(updated_at,1,10) AS day, COUNT(*) as count
        FROM sims
        GROUP BY day
        ORDER BY day ASC
    """)
    return jsonify({
        "labels": [row["day"] for row in rows],
        "counts": [row["count"] for row in rows]
    })

@app.route("/api/sync-status")
def api_sync_status():
    return jsonify(sync_status)


# ===============================
# BACKGROUND LOADER
# ===============================
def background_loader():
    """Pozadinski loader za automatski sync SIM kartica"""
    while True:
        try:
            now_ts = int(time.time())
            next_ts = sync_status.get("next_sync") or 0

            # Pokreni sync samo ako nije u tijeku i ako je prošlo vrijeme
            if not sync_status["running"] and now_ts >= next_ts:
                sync_all_sims()

        except Exception as e:
            print("❌ Background sync error:", e)

        # Provjerava svakih 60 sekundi
        time.sleep(60)


# ===============================
# START APP
# ===============================
if __name__ == "__main__":
    t = threading.Thread(target=background_loader, daemon=True)
    t.start()
    print("📊 Pokrećem dashboard na http://localhost:5000")
    app.run(host="0.0.0.0", port=5000, debug=True)
