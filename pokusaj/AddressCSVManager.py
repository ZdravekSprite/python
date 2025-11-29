from pathlib import Path

class AddressCSVManager:
    def __init__(self, base_folder: str):
        """
        Initialize the manager with a base folder for CSV storage.
        """
        self.base_folder = Path(base_folder)
        self.base_folder.mkdir(parents=True, exist_ok=True)

    @staticmethod
    def addr_part(address: str, part: int = 6) -> str:
        """
        Returns a string combining the hex encoding of the first `part` characters
        of `address` and the original substring.
        """
        prefix_str = address[:part]
        hex_prefix = prefix_str.encode("utf-8").hex()
        return f"{hex_prefix}_{prefix_str}"

    def csv_file_path(self, address: str, part: int = 5) -> Path:
        """
        Build a nested folder path based on prefix segments of `address`,
        ending with a CSV file named from the first `part` characters.
        """
        if part < 2:
            part = 2

        folder = self.base_folder

        if part > 2:
            # First folder: first 2 characters
            folder = folder / address[:2]
            folder.mkdir(exist_ok=True)

            # Subfolders for lengths 3 to part-1
            for length in range(3, part):
                folder = folder / self.addr_part(address, length)
                folder.mkdir(exist_ok=True)

        # Final file path
        filename = self.addr_part(address, part) + ".csv"
        return folder / filename

if __name__ == '__main__':
    from config import REAL_ADDRESSES
    ADDRESSES_FOLDER = str(Path('destination'))
    manager = AddressCSVManager(ADDRESSES_FOLDER)
    for address in REAL_ADDRESSES:
        for i in range(2, 6):
            path = manager.csv_file_path(address, part=i)
            print(path)
