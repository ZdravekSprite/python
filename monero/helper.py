import os
import csv
import datetime as dt
from config import *

def int2hexstr(n:int,c=64):
    return format(n, f'0{c}x')

def int2binstr(n:int,c=42):
    return format(n, f'0{c}b')

def bin2hex(bin):
    "".join(['{:0>2}'.format(hex(e)[2:]) for e in bin])

def path(file,dirs=[]):
    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
    return os.path.sep.join([SCRIPT_DIR]+dirs+[file])

def file_del(file, debug=False):
    if os.path.exists(file):
        os.remove(file)
        print(f"{file} deleted")
    else:
        if debug: print(f"{file} does not exist")
        pass

def file_read(file):
    if os.path.exists(path(file)):
        return open(path(file),"r",encoding="utf-8")
    else:
        print(f"{file} does not exist")
        pass

def csv_reader(csv_file_path):
    csv_list = []
    with open(csv_file_path, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        for row in reader:
            csv_list.append(row)
    return csv_list

def csv_writer(csv_file_path,csv_list):
    with open(csv_file_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for row in csv_list:
            writer.writerow(row)

def csv_dict_reader(csv_file_path):
    csv_list = []
    with open(csv_file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            csv_list.append(row)
    return csv_list

def dict_csv_dict_reader(csv_file_path):
    csv_dict = {}
    with open(csv_file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['address'] in csv_dict.keys():
                if csv_dict[row['address']] != row:
                    print('CHANGE old:',csv_dict[row['address']],'new:',row)
            csv_dict[row['address']] = row
    return csv_dict

def dict_reader(csv_file_path):
    with open(csv_file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
    return reader

def dict_writer(csv_file_path,dict_rows):
    with open(csv_file_path, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=dict_rows.fieldnames)
        writer.writeheader()
        writer.writerows(dict_rows)

def csv_dict_writer(csv_file_path,csv_list,fieldnames=[]): #fieldnames = ['first_name', 'last_name']
    with open(csv_file_path, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        if len(fieldnames): writer.writeheader()
        for row in csv_list:
            writer.writerow(row) #writer.writerow({'first_name': 'Baked', 'last_name': 'Beans'})

def csv_dict_adder(csv_file_path,csv_list,fieldnames=[]): #fieldnames = ['first_name', 'last_name']
    if not os.path.isfile(csv_file_path):
        csv_dict_writer(csv_file_path,[],fieldnames)
    with open(csv_file_path, 'a', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        for row in csv_list:
            writer.writerow(row) #writer.writerow({'first_name': 'Baked', 'last_name': 'Beans'})

def isWin():
    if os.name != 'posix':
        print(os.name)
        #runcmd("dir")
        return True
    else:
        print(os.uname())
        return False

def files_in_dir(dir):
    return next(os.walk(dir), (None, None, []))[2]

def log_files(start:str):
    return [file for file in files_in_dir(path('',['logs'])) if file[:len(start)].lower() == start.lower()]

def address_files(start='4'):
    return [path(file,['address_csv']) for file in files_in_dir(path('',['address_csv'])) if file[:len(start)].lower() == start.lower()]

def test_if_loged(address:str):
    print(address)
    for f in address_files(address[:2]):
        time_print('now: ',[f])
        csv = csv_dict_reader(f)
        for row in csv:
            #address_row address,hex,block,outputs
            if row['address'] == address: return True


def time_print(prefix,data_list):
    print(prefix,dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), " ".join(data_list), " "*10, end='\r')

if __name__ == '__main__':
    print(__file__)
    print(int2binstr(10))
    print(int2hexstr(100))