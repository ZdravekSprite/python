import csv
from pathlib import Path
from typing import Iterator, Optional, List, Dict

class CSVReader:
    def __init__(self, path, fieldnames: Optional[List[str]] = None):
        """
        Initialize CsvReader.
        :param path: Path to CSV file
        :param fieldnames: Optional list of fieldnames (columns). If None, inferred from first row.
        """
        self.path = Path(path)
        # Ensure directory exists
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.fieldnames = fieldnames

    # -----------------------------
    # Read CSV (memory-efficient iterator)
    # -----------------------------
    def read(self) -> Iterator[Dict[str, str]]:
        """
        Read CSV as iterator of dicts (memory-efficient).
        Yields rows one by one.
        """
        if not self.path.exists():
            return iter([])  # empty iterator
        with self.path.open(newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                yield row

    # -----------------------------
    # Read entire CSV into list
    # -----------------------------
    def read_all(self) -> List[Dict[str, str]]:
        """
        Read the entire CSV and return a list of dicts.
        """
        return list(self.read())

if __name__ == '__main__':
    from pathlib import Path
    csv_folder_path = Path('source')
    print(f"Reading CSV from: {csv_folder_path}")

    def folders_sequential(from_folder: Path):
        csv_files = [f for f in from_folder.iterdir() if f.is_file() and f.suffix == '.csv']
        for csv_path in csv_files:
            print(f"Processing file: {csv_path}")
            #for row in CSVReader(csv_path).read():
            #    print(row)
        for subfolder in [f for f in from_folder.iterdir() if f.is_dir()]:
            print(subfolder)
            folders_sequential(subfolder)

    folders_sequential(csv_folder_path)