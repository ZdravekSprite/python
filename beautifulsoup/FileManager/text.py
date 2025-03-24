import os

def isFilePathExists(filePath):
    return os.path.exists(filePath)

def openFilePathForReading(filePath, encoding="windows 1252", create=True):
    if not isFilePathExists(filePath):
        if create:
            f = open(filePath, "w")
            f.close()
        else:
            return f'Datoteka {filePath} ne postoji!'
    
    try:
        return open(filePath, 'r', encoding=encoding)
    except Exception as ex:
        return f'Dogodila se greska prilikom pokusaja otvaranja {filePath} datoteke za citanje! {ex}'

def writeToFilePathOpenClose(filePath, content):
    try:
        with open(filePath, 'w') as fileWriter:
            fileWriter.write(content)
    except Exception as ex:
        return f'Dogodila se greska prilikom pokusaja pisanja u {filePath} datoteku! {ex}'

if __name__ == '__main__':
    print(__file__)

    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
    TXT_FILE = os.path.sep.join([SCRIPT_DIR, 'test.txt'])

    openFilePathForReading(TXT_FILE)
