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

def dir_del(folder, debug=False):
    if (len(files_in_dir(folder))+len(folders_in_dir(folder))) == 0:
        os.rmdir(folder)
        if debug: print(f"{folder} deleted")
        return True
    else:
        if debug: print(f"{folder} not deleted")
        return False

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

def files_path_in_dir(dir):
    files = files_in_dir(dir)
    return [os.path.sep.join([dir,file]) for file in files]

def folders_in_dir(dir):
    return next(os.walk(dir), (None, [], None))[1]

def file_name(address,part=6):
    name = ''
    for c in range(part):
        name+=format(ord(address[c]),f'02x')
    name += '_'+address[:part]
    return name

def addr_csv_file_path(folder,address,fieldnames=[],part=5):
    name = file_name(address,part)
    if not os.path.isdir(folder):
        os.mkdir(folder)
    sub_folder = os.path.sep.join([folder,address[:2]])
    if not os.path.isdir(sub_folder):
        os.mkdir(sub_folder)
    #sub_folders = [address[i:i + 2] for i in range(2, len(address[:part-2]), 2)]
    sub_folders = [address[:i+1] for i in range(2, len(address[:part-1]))]
    for sub_f in sub_folders:
        sub_folder = os.path.sep.join([sub_folder,file_name(sub_f,len(sub_f))])
        if not os.path.isdir(sub_folder):
            os.mkdir(sub_folder)
    csv_file_path = os.path.sep.join([sub_folder,name+'.csv'])
    if not os.path.isfile(csv_file_path):
        with open(csv_file_path, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
    return csv_file_path

if __name__ == '__main__':
    print(__file__)
    address = '47LicRFuuhU2jxUk1XxSqnhcnLNMjgHX35ELKZ2ZoUJWd36dG7oNw955X9rt2HEri3XVioRkdGtFvRBbm1CiuSgZSY2Ka79'
    file_name_1 = file_name(address)
    #print(file_name_1)
    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
    file_path_1 = addr_csv_file_path(SCRIPT_DIR,address)
    print(file_path_1)
    #print(files_path_in_dir(SCRIPT_DIR))
