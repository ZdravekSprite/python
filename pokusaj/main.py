# main.py
import asyncio
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from device_database import DeviceDatabase
from sync_devices import sync_devices, sync_progress

app = FastAPI()
db = DeviceDatabase()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

sync_task = None

@app.get("/")
def dashboard(request: Request, page: int = 1, per_page: int = 10, sort_by: str = "model", filter_model: str = None):
    data = db.get_devices_page(page, per_page, sort_by, filter_model)
    last_sync = db.get_last_sync() or "Never"
    return templates.TemplateResponse("devices.html", {
        "request": request,
        "devices": data["devices"],
        "page": data["page"],
        "total_pages": data["total_pages"],
        "per_page": per_page,
        "sort_by": sort_by,
        "filter_model": filter_model or "",
        "last_sync": last_sync
    })

@app.post("/sync")
async def start_sync():
    """
    Start the background sync if not already running
    """
    global sync_task
    if sync_task is None or sync_task.done():
        loop = asyncio.get_event_loop()
        sync_task = loop.run_in_executor(None, sync_devices)
        return JSONResponse({"status": "started"})
    return JSONResponse({"status": "already running"})

@app.post("/cancel_sync")
async def cancel_sync():
    """
    Request to cancel the ongoing sync
    """
    sync_progress["cancel"] = True
    return JSONResponse({"status": "cancel requested"})

@app.get("/sync_status")
async def get_sync_status():
    """
    Returns the current sync progress
    """
    percent = 0
    if sync_progress["total"]:
        percent = int((sync_progress["fetched"] / sync_progress["total"]) * 100)
    return {
        "status": sync_progress["status"],
        "fetched": sync_progress["fetched"],
        "total": sync_progress["total"],
        "percent": percent
    }
