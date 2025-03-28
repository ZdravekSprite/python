import os
import datetime
from FileManager import *

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_FILE = os.path.sep.join([SCRIPT_DIR, 'EUROJACKPOT.csv'])
NEW_CSV_FILE = os.path.sep.join([SCRIPT_DIR, 'new.csv'])

def sva_kola(file):
    csv_list = []
    csvReaderObject = readCSV(file)
    if type(csvReaderObject) == str:
        print(csvReaderObject)
    else:
        for row in csvReaderObject:
            csv_list.append(row)
    
    #print(csv_list)
    return csv_list

def make_date(datum:str):
    list = datum.split(".")
    return datetime.date(int(list[2]),int(list[1]),int(list[0]))

def make_datetime(datum:str):
    strf = '%d.%m.%Y %H:%M'
    if len(datum.split(" "))==1:
        datum += ' 20:00'
    return datetime.datetime.strptime(datum, strf)

if __name__ == '__main__':
    print(__file__)

    #print(datetime.datetime.strptime('03.01.2023', '%d.%m.%Y'))
    #print(make_date('03.01.2023'))

    #exit()

    list = sva_kola(CSV_FILE)
    list.reverse()
    kolo_no = 0
    new_list = []
    old_year = 0
    for row in list:
        datum = make_date(row[1].split(" ")[1])
        vrijeme = make_datetime(row[1].split(",")[1].strip())
        #new_year = row[1].split(".")[3].split(" ")[0]
        new_year = datum.year
        if new_year==old_year:
            kolo_no += 1
        else:
            kolo_no = 1

        print(new_year,kolo_no,datum,vrijeme,row)
        new_list.append([kolo_no,vrijeme]+[no for no in row[2:]])
        old_year = new_year
    
    new_list.reverse()
    writeCSV(NEW_CSV_FILE, new_list)
