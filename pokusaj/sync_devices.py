# sync_devices.py
import datetime
import time
from teltonika_client import TeltonikaAPI
from device_database import DeviceDatabase

db = DeviceDatabase()
api = TeltonikaAPI()

sync_progress = {"status": "idle", "fetched": 0, "total": 0, "cancel": False}

def sync_devices(page_delay=1):
    """
    Sync devices incrementally to avoid API rate limits.
    page_delay: seconds to wait between pages
    """
    try:
        # First, fetch first page to get total
        first_page = api.get_devices(page=1)
        total_pages = first_page.get("last_page", 1)
        total_devices = first_page.get("total", 0)

        sync_progress.update({
            "status": "syncing",
            "fetched": 0,
            "total": total_devices,
            "cancel": False
        })

        for page in range(1, total_pages + 1):
            if sync_progress["cancel"]:
                sync_progress["status"] = "cancelled"
                return

            data_page = api.get_devices(page=page)
            devices = data_page.get("data", [])
            db.upsert_devices(devices)

            sync_progress["fetched"] += len(devices)
            time.sleep(page_delay)  # avoid hitting quota

        now = datetime.datetime.now(datetime.timezone.utc).isoformat()
        db.set_last_sync(now)
        sync_progress["status"] = "done"

    except Exception as e:
        sync_progress["status"] = f"error: {str(e)}"
