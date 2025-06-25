import os
import csv

def path(file,dirs=[]):
    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
    return os.path.sep.join([SCRIPT_DIR]+dirs+[file])

def file_del(file, debug=False):
    if os.path.exists(file):
        os.remove(file)
        if debug: print(f"{file} deleted")
    else:
        if debug: print(f"{file} does not exist")

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

def csv_adder(csv_file_path,csv_list):
    if not os.path.isfile(csv_file_path):
        with open(csv_file_path, 'w', newline='') as csvfile:
            pass
    with open(csv_file_path, 'a', newline='') as csvfile:
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

def dict_csv_dict_reader(csv_file_path,fieldnames=[]):
    csv_dict = {}
    if not os.path.exists(csv_file_path):
        with open(csv_file_path, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
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
    if not os.path.isdir(os.path.dirname(os.path.abspath(csv_file_path))):
        print(os.path.dirname(os.path.abspath(csv_file_path)),'is not dir')
    else:
        with open(csv_file_path, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            if len(fieldnames): writer.writeheader()
            for row in csv_list:
                writer.writerow(row) #writer.writerow({'first_name': 'Baked', 'last_name': 'Beans'})

def csv_dict_adder(csv_file_path,csv_list,fieldnames=[]): #fieldnames = ['first_name', 'last_name']
    if not os.path.isdir(os.path.dirname(os.path.abspath(csv_file_path))):
        print(os.path.dirname(os.path.abspath(csv_file_path)),'is not dir')
    else:
        if not os.path.isfile(csv_file_path):
            csv_dict_writer(csv_file_path,[],fieldnames)
        with open(csv_file_path, 'a', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            for row in csv_list:
                writer.writerow(row) #writer.writerow({'first_name': 'Baked', 'last_name': 'Beans'})

def files_in_dir(dir):
    return next(os.walk(dir), (None, None, []))[2]

def folders_in_dir(dir):
    return next(os.walk(dir), (None, [], None))[1]


