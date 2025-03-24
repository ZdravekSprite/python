import csv
from .text import openFilePathForReading

def openCsvFilePathForReading(filePath, encoding="windows 1252", create=True, delimiter=";"):
        # reading csv file
        fileReader = openFilePathForReading(filePath, encoding=encoding, create=create)
        if type(fileReader) == str:
            return fileReader
        else:
            # creating a csv reader object
            return csv.reader(fileReader, delimiter=delimiter)

if __name__ == '__main__':
    print(__file__)

    import os
    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
    CSV_FILE = os.path.sep.join([SCRIPT_DIR, 'test.csv'])

    csv_list = []
    csvReaderObject = openCsvFilePathForReading(CSV_FILE)
    if type(csvReaderObject) == str:
        print(csvReaderObject)
    else:
        for row in csvReaderObject:
            csv_list.append(row)
    
    print(csv_list)
