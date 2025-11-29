import csv
from pathlib import Path
from typing import Iterator, Optional, List, Dict

class CSVHandler:
    def __init__(self, path, fieldnames: Optional[List[str]] = None):
        """
        Initialize CSVHandler.
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

    # -----------------------------
    # Write CSV (overwrite)
    # -----------------------------
    def write(self, rows: List[Dict[str, str]]):
        """
        Write rows to CSV (overwrite). If fieldnames are None, infer from first row.
        """
        if not rows:
            if self.fieldnames is None:
                raise ValueError("No rows and no fieldnames provided.")
        else:
            if self.fieldnames is None:
                self.fieldnames = list(rows[0].keys())

        with self.path.open('w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=self.fieldnames)
            writer.writeheader()
            if rows:
                writer.writerows(rows)

    # -----------------------------
    # Append rows to CSV
    # -----------------------------
    def append(self, rows: List[Dict[str, str]]):
        """
        Append rows to CSV. Creates file if it doesn't exist.
        If fieldnames are None, infer from first row or existing CSV.
        """
        if not rows:
            return  # Nothing to append

        file_exists = self.path.exists()

        if self.fieldnames is None:
            self.fieldnames = list(rows[0].keys())

        # If file exists, read headers to confirm fieldnames
        if file_exists:
            with self.path.open(newline='', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                if reader.fieldnames:
                    self.fieldnames = reader.fieldnames

        with self.path.open('a', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=self.fieldnames)
            if not file_exists:
                writer.writeheader()
            writer.writerows(rows)

if __name__ == '__main__':
    from pathlib import Path

    csv_file = "data.csv"
    handler = CSVHandler(csv_file)

    # Write new CSV
    handler.write([{"name": "Alice", "age": "30"}, {"name": "Bob", "age": "25"}])

    # Append new rows
    handler.append([{"name": "Charlie", "age": "35"}])

    # Read CSV (memory-efficient iterator)
    for row in handler.read():
        print(row)

    # Read entire CSV into a list
    all_rows = handler.read_all()
    print(all_rows)
