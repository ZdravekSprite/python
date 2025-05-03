import os
import csv
import datetime as dt

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

def csv_dict_writer(csv_file_path,csv_list,fieldnames=[]): #fieldnames = ['first_name', 'last_name']
    with open(csv_file_path, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        if len(fieldnames): writer.writeheader()
        for row in csv_list:
            writer.writerow(row) #writer.writerow({'first_name': 'Baked', 'last_name': 'Beans'})

def csv_dict_adder(csv_file_path,csv_list,fieldnames=[]): #fieldnames = ['first_name', 'last_name']
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