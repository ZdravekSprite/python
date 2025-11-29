import binascii
import varint
import os
import re
from monero import ed25519
from monero.keccak import keccak_256
from monero.seed import Seed
from pathlib import Path
from CSVReader import CSVReader
from AsyncCSVBatchWriter import AsyncCSVBatchWriter
import concurrent.futures
import threading
import keyboard  # pip install keyboard

# ==============================
# Configuration
# ==============================
from config import REAL_ADDRESSES, FIRST_OUT_DICT, DEBUG, AF_FIELDNAMES, OF_FIELDNAMES
MAX_WORKERS = os.cpu_count() or 2

# Global stop flag
stop_flag = False
total_files_count = 0
total_address_count = 0

#now = datetime.now()
#one_day_ago = now - timedelta(days=1)

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

class MoneroWallet:
    def __init__(self, seed_hex: str = None, block_no= -1, output_no = 0): # type: ignore
        """
        Create a new wallet or restore from existing hex seed.
        """
        if seed_hex:
            self._validate_seed_hex(seed_hex)
            self.seed = Seed(seed_hex)
        else:
            self.seed = Seed()
        self.block_no = block_no
        self.output_no = output_no

    # --- Validation --- #

    @staticmethod
    def _validate_seed_hex(seed_hex: str):
        """
        Validate that the seed hex is exactly 64 hex characters.
        Raises ValueError if invalid.
        """
        if not isinstance(seed_hex, str):
            raise ValueError("Seed hex must be a string.")

        # length check
        if len(seed_hex) != 64:
            raise ValueError(
                f"Seed hex must be 64 hex characters (got {len(seed_hex)})."
            )

        # hex format check
        if not re.fullmatch(r"[0-9a-fA-F]{64}", seed_hex):
            raise ValueError("Seed hex contains invalid characters; must be hex.")

        # final sanity test: ensure Seed() accepts it
        try:
            _ = Seed(seed_hex)
        except Exception as e:
            raise ValueError(f"Seed hex is not structurally valid: {e}")

    # --- Properties --- #

    @property
    def seed_hex(self):
        return self.seed.hex

    @property
    def address(self):
        return str(self.seed.public_address())

    @property
    def public_spend_key(self):
        return str(self.seed.public_spend_key())

    @property
    def public_view_key(self):
        return str(self.seed.public_view_key())

    @property
    def secret_view_key(self):
        return str(self.seed.secret_view_key())

    # --- Export Helpers --- #

    def to_dict(self):
        return {
            'hex': self.seed_hex,
            'address': self.address,
            'svk': self.secret_view_key,
            'psk': self.public_spend_key,
            'block': self.block_no,
            'outputs': self.output_no
        }


class MoneroOutputChecker:
    def __init__(self, confirmed_writer, real_writer, outputs_dict=FIRST_OUT_DICT):
        self.confirmed_writer = confirmed_writer
        self.real_writer = real_writer
        self.outputs_dict = outputs_dict

    # -----------------------------
    # Key & derivation helpers
    # -----------------------------

    @staticmethod
    def generate_key_derivation(pub, sec):
        svk = binascii.unhexlify(sec)
        svk_2 = ed25519.scalar_add(svk, svk)
        svk_4 = ed25519.scalar_add(svk_2, svk_2)
        svk_8 = ed25519.scalar_add(svk_4, svk_4)
        shared_secret = ed25519.scalarmult(svk_8, binascii.unhexlify(pub))
        return shared_secret

    @staticmethod
    def derive_public_key(der, i, spk):
        psk = binascii.unhexlify(spk)
        hsdata = der + varint.encode(i)
        Hs_ur = keccak_256(hsdata).digest()
        Hs = ed25519.scalar_reduce(Hs_ur)
        k = ed25519.edwards_add(ed25519.scalarmult_B(Hs), psk)
        return binascii.hexlify(k).decode()

    # -----------------------------
    # Output checking
    # -----------------------------

    def check_output(self, output_row, address_row):
        pub = output_row['pub']
        sec = address_row['svk']

        # Derivation
        der = self.generate_key_derivation(pub, sec)
        spk = address_row['psk']

        # Derived public key
        derived_pub = self.derive_public_key(der, int(output_row['output_no']), spk)

        # Store "real" addresses if requested
        if self.real_writer and address_row['address'] in REAL_ADDRESSES:
            r_row = {k: address_row[k] for k in address_row if k in self.real_writer.fieldnames}
            self.real_writer.add(r_row)

        # Store confirmed outputs
        if derived_pub == output_row['output_key']:
            confirm_row = {**output_row,
                           'address': address_row['address'],
                           'hex': address_row['hex']}
            self.confirmed_writer.add(confirm_row)

        return derived_pub == output_row['output_key']

    # -----------------------------
    # Address test over many rows
    # -----------------------------

    def test_address(self, csv_row_dict: dict):
        if DEBUG: print(f"\033[K⚠️ Prosessing: {csv_row_dict['hex']}", end='\r')
        for block, output_rows in self.outputs_dict.items():
            if block == csv_row_dict['block'] + 1:
                if DEBUG: print('testing block',block)
                for output_row in output_rows:
                    if DEBUG: print(f"⚠️ Prosessing: {csv_row_dict['hex']}, block {block}, output {output_row['output_no']}", end='\r')
                    if self.check_output(output_row, csv_row_dict):
                        csv_row_dict['outputs'] += 1
                        confirm_row = output_row
                        confirm_row['address']=csv_row_dict['address']
                        confirm_row['hex']=csv_row_dict['hex']
                        confirmed_writer.add(confirm_row)
                    csv_row_dict['block'] = block
        if csv_row_dict['address'] in REAL_ADDRESSES:
            real_writer.add(csv_row_dict)
        return csv_row_dict

def outputs_dict():
    outputs_path = Path('logs/outputs.csv')
    outputs_rows = {}
    for row in CSVReader(outputs_path).read():
        outputs_rows.setdefault(int(row['block_no']), []).append(row)
    return outputs_rows

def process_address(wallet: MoneroWallet, checker: MoneroOutputChecker):
    csv_row = wallet.to_dict()
    if DEBUG: print(csv_row)
    result = checker.test_address(csv_row)
    if DEBUG: print(result)
    result.pop('svk', None)
    result.pop('psk', None)
    return result

def process_csv_file(csv_path: Path, checker: MoneroOutputChecker, debug=False):
    global stop_flag
    global total_address_count
    if stop_flag:
        return
    if debug: print(f"\033[KProcessing file: {csv_path}", end='\r')
    address_rows = CSVReader(csv_path).read_all()  # Read the CSV file rows

    with AsyncCSVBatchWriter(csv_path, fieldnames=AF_FIELDNAMES, batch_size=10) as writer:
        for address in address_rows:
            wallet = MoneroWallet(address['hex'], int(address['block']), int(address['outputs']))
            writer.add(process_address(wallet, checker))
            total_address_count += 1
        # Optional: make sure everything is written before exiting
        writer.flush()
# ==============================
# Folder Processing
# ==============================
def folders_sequential(from_folder: Path, checker: MoneroOutputChecker, debug=False):
    global stop_flag
    global total_files_count
    if stop_flag:
        return 0
    if debug: print(f"\033[KReading CSV from: {from_folder}", end='\r')
    files_count = 0
    futures = []  # Store futures for concurrent tasks

    # Using ThreadPoolExecutor to process files concurrently
    with concurrent.futures.ThreadPoolExecutor() as executor:
        for f in from_folder.iterdir():
            if f.is_file() and f.suffix == '.csv':  # Only process CSV files
                files_count += 1
                total_files_count += 1
                futures.append(executor.submit(process_csv_file, f, checker, debug))
            elif f.is_dir():  # Recursively handle subdirectories
                subfolder = f
                files_count += folders_sequential(subfolder, checker, debug)

        # Wait for all tasks to finish
        for future in concurrent.futures.as_completed(futures):
            try:
                future.result()  # Get the result to ensure any exceptions are raised
            except Exception as e:
                print(f"Error processing file: {e}")

    if debug: print(f"\033[KIn {from_folder} processed {files_count} files.")
    return files_count

if __name__ == '__main__':
    import datetime as dt
    import sys
    # Pomjeri kursor na početak linije
    sys.stdout.write("\033[F")
    # Očisti liniju
    sys.stdout.write("\033[K")
    print("\033[H\033[J", end="")
    print(f"🕒 Start: {dt.datetime.now():%Y-%m-%d %H:%M:%S}")
    confirmed_writer = AsyncCSVBatchWriter('logs/confirmed.csv', OF_FIELDNAMES)
    real_writer = AsyncCSVBatchWriter('logs/real.csv', ['address', 'hex'])
    block_rows = outputs_dict()
    checker = MoneroOutputChecker(confirmed_writer, real_writer, block_rows)

    csv_folder_path = Path('address_csv')
    
    folders_sequential(csv_folder_path, checker, debug=True)  # Enable debug if needed
    
    confirmed_writer.close()
    real_writer.close()
    print(f"Processed {total_files_count} files.")
    print(f"Processed {total_address_count} addresses.")
    print(f"\n✅ Done at {dt.datetime.now():%Y-%m-%d %H:%M:%S}")
