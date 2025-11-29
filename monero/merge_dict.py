import os
import csv
import datetime as dt
from config import real_address
from helper_file import file_del, path, csv_dict_adder

af_fieldnames = ['address','hex','block','outputs']

def add_row_to_dict(dict_,row_,debug=False):
    if row_['address'] in dict_.keys():
        if len(row_['address']) != 95:
            exit
        if len(row_['block']) != 64:
            exit
        if dict_[row_['address']] != row_:
            print('DIFFER:',dict_[row_['address']]['hex'],dict_[row_['address']]['address'],
                  'old:',dict_[row_['address']]['block'],dict_[row_['address']]['outputs'],
                  'new:',row_['block'],row_['outputs'],
                  " "*10, end='\r')
            if dict_[row_['address']]['hex'] != row_['hex']:
                print('DIFFER:',dict_[row_['address']]['address'],
                  'old:',dict_[row_['address']]['hex'],
                  'new:',row_['hex'],
                  " "*10)
            if dict_[row_['address']]['address'] != row_['address']:
                print('DIFFER:',dict_[row_['address']]['hex'],
                  'old:',dict_[row_['address']]['address'],
                  'new:',row_['address'],
                  " "*10)
            if int(dict_[row_['address']]['block']) < int(row_['block']):
                dict_[row_['address']] = row_
                print('DIFFER:',dict_[row_['address']]['hex'],
                  'old:',dict_[row_['address']]['block'],row_['outputs'],
                  'new:',row_['block'],row_['outputs'],
                  " "*10)
        else:
            if debug: print('SAME:',row_," "*10, end='\r')
    else:
        dict_[row_['address']] = row_
    return dict_

def de_x00(addr):
    while True:
        if addr[0]=='\00':
            addr = addr[1:]
        else:
            return addr
        
def create_addr_dict(dict_path,csv_dict={}):
    with open(dict_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile, fieldnames=af_fieldnames)
        for row in reader:
            if row['address'][0]=='\00': row['address'] = de_x00(row['address'])
            if row['address'] in real_address:
                print('real',row)
                csv_file_path = path('real.csv',['logs'])
                csv_dict_adder(csv_file_path,[row],fieldnames=af_fieldnames)
            if row['address'] != 'address': csv_dict = add_row_to_dict(csv_dict, row)
    return csv_dict

def dict_write(dict_path,dict_):
    with open(dict_path, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=af_fieldnames)
        writer.writeheader()
        sorted_values = sorted(dict_.values(), key=lambda d: d['address'])
        writer.writerows(sorted_values)

def merge_addr(from_path,to_path):
    from_files = next(os.walk(from_path), (None, None, []))[2]
    count=0
    files_count=len(from_files)
    start_time = dt.datetime.now()
    for file in from_files:
        
        path_to_dict = os.path.sep.join([to_path,'address_csv',file])
        if not os.path.isfile(path_to_dict):
            with open(path_to_dict.lower(), 'w', newline='') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=af_fieldnames)
                writer.writeheader()
        err = False
        csv_dict = {}
        try:
            csv_dict_new = create_addr_dict(path_to_dict,csv_dict)
            csv_dict = csv_dict_new
        except Exception as ex:
            err = True
            print(ex)
        delta_count = len(csv_dict)

        path_from_dict = os.path.sep.join([from_path,file])
        try:
            csv_dict_new = create_addr_dict(path_from_dict,csv_dict)
            csv_dict = csv_dict_new
        except Exception as ex:
            err = True
            print(ex)
        dict_write(path_to_dict,csv_dict)

        delta_count = len(csv_dict)-delta_count
        count+=len(csv_dict)
        now_time = dt.datetime.now()
        delta = now_time - start_time
        print("now: ",files_count,dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), file, f"{count:,}", int(delta_count//delta.total_seconds()), " "*10, end='\r')
        start_time = dt.datetime.now()
        if not err:
            file_del(path_from_dict)
            files_count-=1
    print()

if __name__ == '__main__':
    print(__file__)
    from_dict_path = "c:\\monero\\address_csv_1"
    from_dict_path = "/home/zdravek/projects/monero/address_csv_1/"
    to_path = "c:\\monero"
    to_path = "/home/zdravek/projects/monero/"
    print('start:',dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    #from_dict_path = "/home/zdravek/projects/python/monero/address_csv/"
    #merge_addr(from_dict_path,to_path)
    from_dict_path = "/home/zdravek/projects/monero/address_csv_1/"
    merge_addr(from_dict_path,to_path)
    #from_dict_path = "/home/zdravek/projects/monero/address_csv_2/"
    #merge_addr(from_dict_path,to_path)

    print('end:  ',dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),' '*10)