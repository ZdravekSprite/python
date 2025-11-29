import sqlite3
from datetime import datetime

db_path = "devices.db"

def init_db():
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS devices (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        imei TEXT,
        model TEXT,
        modem_version TEXT,
        activity_status TEXT,
        last_seen TEXT
    )""")
    cur.execute("""
    CREATE TABLE IF NOT EXISTS sync_log (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        last_sync TEXT
    )""")
    conn.commit()
    conn.close()


def get_last_sync():
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute("SELECT last_sync FROM sync_log ORDER BY id DESC LIMIT 1")
    row = cur.fetchone()
    conn.close()
    return row[0] if row else None


def set_last_sync():
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    now = datetime.now().isoformat()
    cur.execute("INSERT INTO sync_log (last_sync) VALUES (?)", (now,))
    conn.commit()
    conn.close()


def count_devices_to_sync():
    # placeholder: return total number of devices to sync
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM devices")
    total = cur.fetchone()[0]
    conn.close()
    return total


def sync_devices(progress_callback=None):
    """
    Dummy sync function.
    Replace with actual API calls to fetch devices and insert/update DB.
    """
    import time
    total = 100  # simulate 100 devices
    for i in range(1, total+1):
        if progress_callback:
            progress_callback(i, total)
        time.sleep(0.05)  # simulate delay per device
    set_last_sync()
