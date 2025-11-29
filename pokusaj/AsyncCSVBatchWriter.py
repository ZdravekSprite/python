from pathlib import Path
import csv
import threading
from queue import Queue, Empty
import time
import tempfile
import shutil
from config import BATCH_SIZE, OF_FIELDNAMES

class AsyncCSVBatchWriter:
    def __init__(self, file_path, fieldnames, batch_size=BATCH_SIZE, flush_interval=1.0, sort_key='address'):
        self.file_path = Path(file_path)
        self.fieldnames = fieldnames
        self.batch_size = batch_size
        self.flush_interval = flush_interval
        self.sort_key = sort_key  # now sorting by address

        self.queue = Queue()
        self.stop_event = threading.Event()
        self.lock = threading.Lock()

        self.file_path.parent.mkdir(parents=True, exist_ok=True)

        if not self.file_path.is_file():
            with self.file_path.open('w', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=self.fieldnames)
                writer.writeheader()

        # Load existing rows
        self.latest_rows = {}
        with self.file_path.open('r', newline='') as f:
            for row in csv.DictReader(f):
                key = row['address']
                self.latest_rows[key] = row

        self.dirty_keys = set()
        self.worker_thread = threading.Thread(target=self._worker, daemon=True)
        self.worker_thread.start()

    def add(self, row):
        row = row.copy()
        address = row['address']
        block = int(row['block'])  # keep largest block

        with self.lock:
            if address in self.latest_rows:
                existing_block = int(self.latest_rows[address]['block'])
                if block <= existing_block:
                    return  # skip smaller block
            self.latest_rows[address] = row
            self.dirty_keys.add(address)

        self.queue.put(address)

    def _worker(self):
        last_flush = time.monotonic()
        pending_keys = set()

        while True:
            if self.stop_event.is_set() and self.queue.empty():
                break

            try:
                key = self.queue.get(timeout=0.1)
                pending_keys.add(key)
                self.queue.task_done()

                if len(pending_keys) >= self.batch_size:
                    self._flush()
                    pending_keys.clear()
                    last_flush = time.monotonic()

            except Empty:
                if pending_keys and (time.monotonic() - last_flush) >= self.flush_interval:
                    self._flush()
                    pending_keys.clear()
                    last_flush = time.monotonic()

        if pending_keys:
            self._flush()

    def _flush(self):
        with self.lock:
            if not self.dirty_keys:
                return

            all_rows = list(self.latest_rows.values())

            # Sort by address for readability
            all_rows.sort(key=lambda r: r[self.sort_key])

            temp_file = tempfile.NamedTemporaryFile('w', newline='', delete=False)
            with temp_file:
                writer = csv.DictWriter(temp_file, fieldnames=self.fieldnames)
                writer.writeheader()
                writer.writerows(all_rows)

            shutil.move(temp_file.name, self.file_path)
            self.dirty_keys.clear()

    def flush(self):
        self.queue.join()
        self._flush()

    def close(self):
        self.flush()
        self.stop_event.set()
        self.worker_thread.join()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        self.close()

import random

# ----------------------------------------------------------------------
# Example usage
# ----------------------------------------------------------------------
if __name__ == "__main__":
    from config import OF_FIELDNAMES

    with AsyncCSVBatchWriter("proba/test/data.csv", fieldnames=OF_FIELDNAMES, batch_size=10) as writer:
        for i in range(500):
            address = f"addr_{random.randint(0, 99):04d}"  # some addresses may repeat
            writer.add({
                "address": address,
                "hex": hex(random.randint(0, 2**64)),
                "block": random.randint(1, 100),
                "outputs": random.randint(0, 500)
            })

        # Optional: make sure everything is written before exiting
        writer.flush()
    print("CSV writing complete. Check 'proba/test/data.csv'")
