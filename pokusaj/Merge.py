import os
from pathlib import Path
from CSVReader import CSVReader
from AsyncCSVBatchWriter import AsyncCSVBatchWriter
from AddressCSVManager import AddressCSVManager
ADDRESSES_FOLDER = str(Path('destination'))
manager = AddressCSVManager(ADDRESSES_FOLDER)
fieldnames = ['address', 'hex', 'block', 'outputs']
DEBUG = True
MAX_WORKERS = os.cpu_count() or 2

from concurrent.futures import ThreadPoolExecutor

def folders_parallel(from_folder: Path, executor: ThreadPoolExecutor, debug=True):
    if debug:
        print(f"Processing folder: {from_folder}")

    # Collect csv files
    csv_files = [f for f in from_folder.iterdir() if f.is_file() and f.suffix == ".csv"]

    futures = []

    # Submit parallel tasks
    for csv_path in csv_files:
        if debug:
            print(f"Submitting file: {csv_path}")
        futures.append(executor.submit(process_file, csv_path, debug))

    # WAIT until all files in THIS folder are processed
    for f in futures:
        f.result()   # blocks until the worker finishes

    # Recurse into subfolders AFTER processing local files
    for subfolder in [f for f in from_folder.iterdir() if f.is_dir()]:
        folders_parallel(subfolder, executor, debug)

    # Now it's safe to delete folder if empty
    delete_dir_if_empty(from_folder, debug)

def run_parallel(root: Path, workers=MAX_WORKERS):
    with ThreadPoolExecutor(max_workers=workers) as executor:
        folders_parallel(root, executor)

# ==============================
# Basic Utilities
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
    try:
        if path.exists() and not any(path.iterdir()):
            path.rmdir()
            if debug:
                print(f"🧹 Deleted empty directory: {path}")
        else:
            if debug:
                print(f"⏹️ Directory not empty, skipped deletion: {path}")
    except Exception as e:
        if debug:
            print(f"⚠️ Cannot delete directory {path}: {e}")

def process_file(csv_path: Path, debug=DEBUG):
        file_rows = {}
        if debug:
            print(f"Processing file: {csv_path}", end='\r')
        for row in CSVReader(csv_path).read():
            #print(row)
            path = manager.csv_file_path(row['address'], part=5)
            file_rows.setdefault(path, []).append(row)
            #print(path)
        if debug:
            print(f"End processing file: {csv_path}")
        #print("Folders rows:", folder_rows.keys())
        for path, rows in file_rows.items():
            if debug:
                print(f"File: {path}, Rows count: {len(rows)}")
            with AsyncCSVBatchWriter(path, fieldnames=fieldnames, batch_size=100) as writer:
                    for r in rows:
                        writer.add(r)
                    # Optional: make sure everything is written before exiting
                    writer.flush()
        delete_file(csv_path)

def folders_sequential(from_folder: Path, debug=DEBUG):
    if debug:
        print(f"Processing filder: {from_folder}")
    csv_files = [f for f in from_folder.iterdir() if f.is_file() and f.suffix == '.csv']
    for csv_path in csv_files:
        process_file(csv_path)
    for subfolder in [f for f in from_folder.iterdir() if f.is_dir()]:
        folders_sequential(subfolder)
    delete_dir_if_empty(from_folder)

if __name__ == '__main__':
    csv_folder_path = Path('source')
    print(f"Reading CSV from: {csv_folder_path}")
    #folders_sequential(csv_folder_path)
    run_parallel(csv_folder_path)
    ensure_dir(csv_folder_path)