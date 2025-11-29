import os
from pathlib import Path
from CSVReader import CSVReader
from AsyncCSVBatchWriter import AsyncCSVBatchWriter
from AddressCSVManager import AddressCSVManager
from concurrent.futures import ThreadPoolExecutor
import threading
import keyboard  # pip install keyboard

# ==============================
# Configuration
# ==============================
ADDRESSES_FOLDER = str(Path('destination'))
manager = AddressCSVManager(ADDRESSES_FOLDER)
fieldnames = ['address', 'hex', 'block', 'outputs']
DEBUG = False
MAX_WORKERS = os.cpu_count() or 2

# Global stop flag
stop_flag = False

# ==============================
# Keyboard Listener
# ==============================
def listen_for_space():
    global stop_flag
    keyboard.wait('space')
    print("\n⛔ SPACE pressed — stopping...")
    stop_flag = True

# Start the listener in a daemon thread
threading.Thread(target=listen_for_space, daemon=True).start()

# ==============================
# Utilities
# ==============================
def ensure_dir(path: Path):
    path.mkdir(parents=True, exist_ok=True)

def delete_file(path: Path, debug=DEBUG):
    try:
        if path.exists():
            path.unlink()
            if debug:
                print(f"🗑️ Deleted file: {path}", end='\r')
    except PermissionError as e:
        if debug:
            print(f"⚠️ Cannot delete {path}: {e}")

def delete_dir_if_empty(path: Path, debug=DEBUG):
    debug=True
    try:
        if path.exists() and not any(path.iterdir()):
            path.rmdir()
            if debug:
                print(f"🧹 Deleted empty directory: {path}", end='\r')
        else:
            if debug:
                print(f"⏹️ Directory not empty, skipped deletion: {path}")
    except Exception as e:
        if debug:
            print(f"⚠️ Cannot delete directory {path}: {e}")

# ==============================
# File Processing
# ==============================
def process_file(csv_path: Path, debug=DEBUG):
    global stop_flag
    if stop_flag:
        return

    file_rows = {}
    if debug:
        print(f"Processing file: {csv_path}", end='\r')

    for row in CSVReader(csv_path).read():
        if stop_flag:
            return
        path = manager.csv_file_path(row['address'], part=5)
        file_rows.setdefault(path, []).append(row)

    if debug:
        print(f"End processing file: {csv_path}")

    for path, rows in file_rows.items():
        if stop_flag:
            return
        if debug:
            print(f"File: {path}, Rows count: {len(rows)}")
        with AsyncCSVBatchWriter(path, fieldnames=fieldnames, batch_size=100) as writer:
            for r in rows:
                if stop_flag:
                    return
                writer.add(r)
            writer.flush()

    if not stop_flag:
        delete_file(csv_path, debug)

# ==============================
# Folder Processing
# ==============================
def folders_parallel(from_folder: Path, executor: ThreadPoolExecutor, debug=DEBUG):
    global stop_flag
    if stop_flag:
        return
    if debug:
        print(f"Processing folder: {from_folder}")
    
    futures = []
    for f in from_folder.iterdir():
        if stop_flag:
            return
        if f.is_file() and f.suffix == ".csv":
            csv_path = f
            if debug:
                print(f"Submitting file: {csv_path}")
            futures.append(executor.submit(process_file, csv_path, debug))
        if f.is_dir():
            subfolder = f
            folders_parallel(subfolder, executor, debug)
    for f in futures:
        if stop_flag:
            return
        f.result()
    if not stop_flag:
        delete_dir_if_empty(from_folder, debug)

def run_parallel(root: Path, workers=MAX_WORKERS):
    with ThreadPoolExecutor(max_workers=workers) as executor:
        folders_parallel(root, executor)

# ==============================
# Main
# ==============================
if __name__ == '__main__':
    import datetime as dt
    print(f"🕒 Start: {dt.datetime.now():%Y-%m-%d %H:%M:%S}")
    csv_folder_path = Path('source')
    print(f"Reading CSV from: {csv_folder_path}")
    run_parallel(csv_folder_path)
    ensure_dir(csv_folder_path)
    print(f"\n✅ Done at {dt.datetime.now():%Y-%m-%d %H:%M:%S}")
