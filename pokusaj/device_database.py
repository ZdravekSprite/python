# device_database.py
import sqlite3
import os
from math import ceil

DB_FILE = os.path.join(os.path.dirname(__file__), "teltonika_devices.db")

class DeviceDatabase:
    def __init__(self, db_path=DB_FILE):
        self.db_path = db_path
        self._create_table()

    def _create_table(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS devices (
                    imei TEXT PRIMARY KEY,
                    model TEXT,
                    modem_version TEXT,
                    activity_status TEXT,
                    last_seen TEXT,
                    current_configuration TEXT,
                    current_firmware TEXT
                )
            """)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS metadata (
                    key TEXT PRIMARY KEY,
                    value TEXT
                )
            """)

    def upsert_devices(self, devices):
        with sqlite3.connect(self.db_path) as conn:
            for d in devices:
                conn.execute("""
                    INSERT INTO devices (
                        imei, model, modem_version, activity_status, last_seen,
                        current_configuration, current_firmware
                    ) VALUES (?, ?, ?, ?, ?, ?, ?)
                    ON CONFLICT(imei) DO UPDATE SET
                        model=excluded.model,
                        modem_version=excluded.modem_version,
                        activity_status=excluded.activity_status,
                        last_seen=excluded.last_seen,
                        current_configuration=excluded.current_configuration,
                        current_firmware=excluded.current_firmware
                """, (
                    str(d.get("imei", "")),
                    d.get("model", ""),
                    d.get("modem_version", ""),
                    d.get("activity_status", ""),
                    d.get("seen_at", ""),
                    d.get("current_configuration", ""),
                    d.get("current_firmware", "")
                ))

    def get_last_sync(self):
        with sqlite3.connect(self.db_path) as conn:
            cur = conn.cursor()
            cur.execute("SELECT value FROM metadata WHERE key='last_sync'")
            row = cur.fetchone()
            return row[0] if row else None

    def set_last_sync(self, timestamp):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                INSERT INTO metadata (key, value)
                VALUES ('last_sync', ?)
                ON CONFLICT(key) DO UPDATE SET value=excluded.value
            """, (timestamp,))

    def get_devices_page(self, page=1, per_page=10, sort_by="model", filter_model=None):
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()

            where_clause = ""
            params = []
            if filter_model:
                where_clause = "WHERE model LIKE ?"
                params.append(f"%{filter_model}%")

            # total count
            cur.execute(f"SELECT COUNT(*) FROM devices {where_clause}", params)
            total = cur.fetchone()[0]

            total_pages = max(ceil(total / per_page), 1)
            offset = (page - 1) * per_page

            cur.execute(f"""
                SELECT imei, model, modem_version, activity_status, last_seen,
                       current_configuration, current_firmware
                FROM devices
                {where_clause}
                ORDER BY {sort_by} COLLATE NOCASE
                LIMIT ? OFFSET ?
            """, params + [per_page, offset])

            devices = [dict(row) for row in cur.fetchall()]
            return {
                "devices": devices,
                "page": page,
                "total_pages": total_pages
            }
