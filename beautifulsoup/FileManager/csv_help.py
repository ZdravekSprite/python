import csv
if __name__ == '__main__':
    from text import openFilePathForReading
else:
    from .text import openFilePathForReading

def openCsvFilePathForReading(filePath, encoding="windows 1252", create=True, delimiter=";"):
        # reading csv file
        fileReader = openFilePathForReading(filePath, encoding=encoding, create=create)
        if type(fileReader) == str:
            return fileReader
        else:
            # creating a csv reader object
            return csv.reader(fileReader, delimiter=delimiter)

def write2CsvFilePath(filePath, csv_rows, csv_fields=[], encoding="windows 1252", delimiter=";"):
    # writing to csv file
    with open(filePath, 'w', encoding=encoding) as csvfile:
        # creating a csv writer object
        csvwriter = csv.writer(csvfile, delimiter=delimiter, lineterminator='\n')
        # writing the fields
        if len(csv_fields):
            csvwriter.writerow(csv_fields)
        # writing the data rows
        csvwriter.writerows(csv_rows)

def append2CsvFilePath(filePath, csv_rows, encoding="windows 1252", delimiter=";"):
    # writing to csv file
    with open(filePath, 'a', encoding=encoding) as csvfile:
        # creating a csv writer object
        csvwriter = csv.writer(csvfile, delimiter=delimiter, lineterminator='\n')
        # writing the data rows
        csvwriter.writerows(csv_rows)

if __name__ == '__main__':
    print(__file__)

    import os
    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
    CSV_FILE = os.path.sep.join([SCRIPT_DIR, 'test.csv'])
    NEW_FILE = os.path.sep.join([SCRIPT_DIR, 'new.csv'])

    csv_list = []
    csvReaderObject = openCsvFilePathForReading(CSV_FILE)
    if type(csvReaderObject) == str:
        print(csvReaderObject)
    else:
        for row in csvReaderObject:
            csv_list.append(row)
    
    print(csv_list)

    write2CsvFilePath(NEW_FILE, [['test5', 'test6'], ['test7', 'test8']], ['A', 'B'])
    append2CsvFilePath(NEW_FILE, [['test9', 'test10'], ['test11', 'test12']])