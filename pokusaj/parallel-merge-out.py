import csv
import os
import datetime as dt
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from collections import defaultdict
import threading
from threading import Lock, Event, Thread
from config import real_address, SOURCE_FOLDER  # must define this list or set
import keyboard  # for detecting space key
# --- Monero imports ---
import binascii
import varint
from monero.seed import Seed
from monero import ed25519
from monero.keccak import keccak_256


# ==============================
# Config
# ==============================

AF_FIELDNAMES = ['address', 'hex', 'block', 'outputs']
MAX_WORKERS = os.cpu_count() or 4
DEBUG = True  # Set False to turn off debug logs
BATCH_SIZE = 10

# ==============================
# Global Stop Event
# ==============================

stop_event = Event()

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


# -------------------------
# CSV Helper Classes
# -------------------------
class CsvBatchWriter:
    """Batch CSV writer with thread-safe writes."""
    def __init__(self, file_path, fieldnames, batch_size=BATCH_SIZE):
        self.file_path = file_path
        self.fieldnames = fieldnames
        self.batch_size = batch_size
        self.buffer = []
        self.lock = threading.Lock()
        # Ensure CSV exists with header
        if not os.path.isfile(file_path):
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, 'w', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()

    def add(self, row):
        del row['svk']
        del row['psk']
        self.buffer.append(row)
        if len(self.buffer) >= self.batch_size:
            self.flush()

    def flush(self):
        with self.lock:
            if self.buffer:
                with open(self.file_path, 'a', newline='') as f:
                    writer = csv.DictWriter(f, fieldnames=self.fieldnames)
                    for row in self.buffer:
                        writer.writerow(row)
                self.buffer = []

# ==============================
# CSV Utilities
# ==============================

def read_csv_dict(path: Path) -> list[dict]:
    if not path.exists():
        return []
    with path.open(newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        return list(reader)

def write_csv_dict(path: Path, rows: list[dict], fieldnames=AF_FIELDNAMES):
    ensure_dir(path.parent)
    with path.open('w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

def append_csv_dict(path: Path, rows: list[dict], fieldnames=AF_FIELDNAMES):
    ensure_dir(path.parent)
    file_exists = path.exists()
    with path.open('a', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        writer.writerows(rows)

# ==============================
# Address Helpers
# ==============================

def file_name(address: str, part: int = 6) -> str:
    hex_part = ''.join(format(ord(c), '02x') for c in address[:part])
    return f"{hex_part}_{address[:part]}"

def addr_csv_path(base_folder: Path, address: str, fieldnames=AF_FIELDNAMES, part: int = 5) -> Path:
    name = file_name(address, part)
    sub_folder = base_folder / address[:2]

    ensure_dir(sub_folder)
    for i in range(2, len(address[:part - 1])):
        sub_folder = sub_folder / file_name(address[:i + 1], len(address[:i + 1]))
        ensure_dir(sub_folder)

    csv_path = sub_folder / f"{name}.csv"
    if not csv_path.exists():
        write_csv_dict(csv_path, [], fieldnames)
    return csv_path

def add_row_to_dict(d: dict, row: dict) -> dict:
    addr = row['address']
    if len(addr) != 95 or not row['block']:
        return d
    existing = d.get(addr)
    if existing:
        if int(existing['block']) < int(row['block']):
            d[addr] = row
    else:
        d[addr] = row
    return d

# -------------------------
# Crypto / Monero Logic
# -------------------------

af_fieldnames = ['address','hex','block','outputs']
c_fieldnames = ['block_no','transaction_hash','pub','output_no','output_key','address','hex']

def rnd_seed():
    seed = Seed()
    seed.public_spend_key()
    seed.public_view_key()
    return seed

def generate_key_derivation(pub, sec):
    svk = binascii.unhexlify(sec)
    svk_2 = ed25519.scalar_add(svk, svk)
    svk_4 = ed25519.scalar_add(svk_2, svk_2)
    svk_8 = ed25519.scalar_add(svk_4, svk_4)
    shared_secret = ed25519.scalarmult(svk_8, binascii.unhexlify(pub))
    return shared_secret

def derive_public_key(der, i, spk):
    shared_secret = der
    psk = binascii.unhexlify(spk)
    hsdata = shared_secret + varint.encode(i)
    Hs_ur = keccak_256(hsdata).digest()
    Hs = ed25519.scalar_reduce(Hs_ur)
    k = ed25519.edwards_add(ed25519.scalarmult_B(Hs), psk)
    return binascii.hexlify(k).decode()

def check_output(output_row, address_row, confirmed_writer, real_writer=None):
    pub = output_row['pub']
    sec = address_row['svk']
    der = generate_key_derivation(pub, sec)
    spk = address_row['psk']
    pubkey = derive_public_key(der, int(output_row['output_no']), spk)
    #del address_row['svk']
    #del address_row['psk']

    # Record real addresses
    if real_writer and address_row['address'] in real_address:
        r_row = {k: address_row[k] for k in address_row if k in real_writer.fieldnames}
        real_writer.add(r_row)

    # Record confirmed outputs
    if pubkey == output_row['output_key']:
        confirm_row = {**output_row, 'address': address_row['address'], 'hex': address_row['hex']}
        confirmed_writer.add(confirm_row)

    return pubkey == output_row['output_key']

# -------------------------
# address testing
# -------------------------
def test_address(csv_row_dict, target_block_rows, confirmed_writer, real_writer=None):
    seed = Seed(csv_row_dict['hex'])
    #print(Seed().__dict__.keys()) # dict_keys(['phrase', 'hex', 'word_list', '_ed_pub_spend_key', '_ed_pub_view_key'])
    seed.public_spend_key()
    seed.public_view_key()
    csv_row_dict = {
        'hex': seed.hex,
        'address': str(seed.public_address()),
        'svk': str(seed.secret_view_key()),
        'psk': str(seed.public_spend_key()),
        'block': -1,
        'outputs': 0
    }
    for target_row in target_block_rows:
        if check_output(target_row, csv_row_dict, confirmed_writer, real_writer):
            csv_row_dict['outputs'] += 1
        csv_row_dict['block'] = target_row['block_no']
    del csv_row_dict['svk']
    del csv_row_dict['psk']
    return csv_row_dict

# ==============================
# Merge Logic
# ==============================

file_locks = defaultdict(Lock)

def process_csv_file(csv_path: Path, output_folder: Path):
    if stop_event.is_set():
        return 0

    csv_files_dict = {}
    rows_merged = 0
    fully_processed = True

    with csv_path.open(newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if stop_event.is_set():
                print(f"\n⚠️ Stop requested during processing {csv_path.name}")
                fully_processed = False
                break

            addr = row.get('address')
            if not addr or row['address'] == 'address':
                continue

            addr = addr.lstrip('\x00')
            row['address'] = addr

            # Check if block is greater than 1
            try:
                block = int(row.get('block', 0))  # Convert 'block' to an integer, default to 0
                if block <= 1:
                    row = test_address(row, target_block_rows, confirmed_writer, real_writer)
                    #continue  # Skip rows where block is 1 or less
            except ValueError:
                print(f"⚠️ Invalid block value in row: {row}")
                #continue  # Skip if block is not a valid integer

            if addr in real_address:
                append_csv_dict(Path('logs/real.csv'), [row])

            file_path = addr_csv_path(output_folder, addr)

            if file_path not in csv_files_dict:
                existing_rows = read_csv_dict(file_path) if file_path.exists() else []
                csv_files_dict[file_path] = {r['address']: r for r in existing_rows}

            csv_files_dict[file_path] = add_row_to_dict(csv_files_dict[file_path], row)
            rows_merged += 1

    # Write merged data
    for out_path, data_dict in csv_files_dict.items():
        with file_locks[str(out_path)]:
            if out_path.exists():
                existing_rows = read_csv_dict(out_path)
                temp_dict = {r['address']: r for r in existing_rows}
                temp_dict.update(data_dict)
                write_csv_dict(out_path, list(temp_dict.values()))
            else:
                write_csv_dict(out_path, list(data_dict.values()))

    if fully_processed:
        delete_file(csv_path, debug=DEBUG)

    return rows_merged

def merge_files_in_folder(from_folder: Path, to_folder: Path):
    if stop_event.is_set():
        return 0, 0, 0.0

    csv_files = [f for f in from_folder.iterdir() if f.is_file() and not f.name.startswith('_')]

    if not csv_files:
        return 0, 0, 0.0

    folder_start = dt.datetime.now()
    total_rows = 0

    # Parallel processing for files only
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = {executor.submit(process_csv_file, f, to_folder): f for f in csv_files}
        for future in as_completed(futures):
            if stop_event.is_set():
                print("\n⚠️ Stopping remaining files due to user request...")
                break
            try:
                total_rows += future.result()
            except Exception as e:
                print(f"[ERROR] File {futures[future]}: {e}")

    folder_elapsed = (dt.datetime.now() - folder_start).total_seconds()
    print(f"\n📂 Folder '{from_folder}' processed: {len(csv_files)} files, {total_rows} rows, {folder_elapsed:.1f}s")
    return len(csv_files), total_rows, folder_elapsed

# ==============================
# Summary Helper
# ==============================

def write_summary(folder: Path, files_count: int, rows_count: int, elapsed: float):
    summary_folder = Path("merge_summaries")
    ensure_dir(summary_folder)
    summary_path = summary_folder / "folder_summary.csv"
    
    existing = read_csv_dict(summary_path)
    
    if files_count > 5:
        existing.append({
            'folder': str(folder),
            'files_count': files_count,
            'rows_count': rows_count,
            'elapsed_seconds': f"{elapsed:.2f}"
        })
    
    # Remove old TOTAL row
    existing = [row for row in existing if row.get('folder') != 'TOTAL']

    total_files = sum(int(row['files_count']) for row in existing)
    total_rows = sum(int(row['rows_count']) for row in existing)
    total_elapsed = sum(float(row['elapsed_seconds']) for row in existing)

    existing.append({
        'folder': 'TOTAL',
        'files_count': total_files,
        'rows_count': total_rows,
        'elapsed_seconds': f"{total_elapsed:.2f}"
    })

    write_csv_dict(summary_path, existing, fieldnames=['folder', 'files_count', 'rows_count', 'elapsed_seconds'])

# ==============================
# Merge Folder Sequentially
# ==============================

def merge_folders_sequential(from_folder: Path, to_folder: Path):
    if stop_event.is_set():
        return 0, 0, 0.0

    total_files, total_rows, total_elapsed = merge_files_in_folder(from_folder, to_folder)

    for subfolder in [f for f in from_folder.iterdir() if f.is_dir()]:
        if stop_event.is_set():
            print(f"\n⚠️ Stop requested. Skipping remaining subfolders in '{from_folder}'...")
            break
        f_count, r_count, f_elapsed = merge_folders_sequential(subfolder, to_folder)
        total_files += f_count
        total_rows += r_count
        total_elapsed += f_elapsed

    delete_dir_if_empty(from_folder)
    write_summary(from_folder, total_files, total_rows, total_elapsed)
    print(f"[DONE]  {from_folder}: {total_files} files, {total_rows} rows total")
    return total_files, total_rows, total_elapsed

# ==============================
# Key Listener
# ==============================

def listen_for_stop():
    print("Press SPACE to stop the script gracefully...")
    keyboard.wait('space')
    print("\n⏹️ Stop requested by user!")
    stop_event.set()

# ==============================
# Main Entry
# ==============================

if __name__ == '__main__':
    #TO_PATH = Path("destination")
    TO_PATH = Path(SOURCE_FOLDER)
    FROM_PATH = Path("source/test")

    # CSV writers for confirmed outputs and real addresses
    os.makedirs('logs', exist_ok=True)
    confirmed_writer = CsvBatchWriter('logs/confirmed.csv', c_fieldnames, batch_size=BATCH_SIZE)
    real_writer = CsvBatchWriter('logs/real.csv', ['address','hex'], batch_size=BATCH_SIZE)
    target_block_rows = read_csv_dict(Path("logs/outputs.csv"))

    listener_thread = Thread(target=listen_for_stop, daemon=True)
    listener_thread.start()

    start_time = dt.datetime.now()
    print(f"🕒 Start: {start_time:%Y-%m-%d %H:%M:%S}")

    total_files, total_rows, elapsed_total = merge_folders_sequential(FROM_PATH, TO_PATH)

    if stop_event.is_set():
        print(f"\n⚠️ Script stopped by user. Partial merges may exist.")
    else:
        print(f"\n✅ Done at {dt.datetime.now():%Y-%m-%d %H:%M:%S}")

    print(f"Total files merged: {total_files}, total rows merged: {total_rows}, total time: {elapsed_total:.1f}s")
