import os
import csv
import datetime as dt
from helper_file import *
from helper import time_print
from merge_dict import add_row_to_dict
from config import real_address

af_fieldnames = ['address','hex','block','outputs']

def csv_file_path(folder,address):
    name = file_name(address)
    if not os.path.isdir(folder):
        os.mkdir(folder)
    sub_folder = os.path.sep.join([folder,address[:2]])
    if not os.path.isdir(sub_folder):
        os.mkdir(sub_folder)
    csv_file_path = os.path.sep.join([sub_folder,name+'.csv'])
    if not os.path.isfile(csv_file_path):
        with open(csv_file_path, 'w', newline='') as csvfile:
            pass
    return csv_file_path

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

def create_addr_dict_with_files(dict_path,to_path,csv_files_dict={}):
    with open(dict_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile, fieldnames=af_fieldnames)
        for row in reader:
            if row['address'][0]=='\00': row['address'] = de_x00(row['address'])
            if row['address'] in real_address:
                print('real',row)
                csv_file_path = path('real.csv',['logs'])
                csv_dict_adder(csv_file_path,[row],fieldnames=af_fieldnames)
            if row['address'] != 'address':
                file_path = addr_csv_file_path(to_path,row['address'],af_fieldnames)
                if file_path not in csv_files_dict.keys():
                    #print(file_path)
                    csv_files_dict[file_path] = {} #create_addr_dict(file_path)
                csv_files_dict[file_path] = add_row_to_dict(csv_files_dict[file_path], row)
    return csv_files_dict

def merge_files(from_path,to_path):
    print(from_path)
    print(to_path)
    from_files = files_in_dir(from_path)
    #import random
    #random.shuffle(from_files)
    files_count = len(from_files)
    start_time = dt.datetime.now()
    for file in from_files:
        if file[:1] != "_":
            from_file_path = os.path.sep.join([from_path,file])
            #print(from_file_path)
            #time_print('now:  ',[from_file_path,str(file_count)])
            new_csv_files_dict = create_addr_dict_with_files(from_file_path,to_path,{})
            '''
            with open(from_file_path, newline='') as csvfile:
                reader = csv.DictReader(csvfile, fieldnames=af_fieldnames)
                for row in reader:
                    if row['address'][0]=='\00': row['address'] = de_x00(row['address'])
                    if row['address'] in real_address:
                        print('real',row)
                        csv_file_path = path('real.csv',['logs'])
                        csv_dict_adder(csv_file_path,[row],fieldnames=af_fieldnames)
                    if row['address'] != 'address':
                        #print(row['address'])
                        to_file_path = addr_csv_file_path(to_path,row['address'],af_fieldnames)
                        #print(to_file_path)
                        with open(to_file_path, 'a', newline='') as csvfile:
                            writer = csv.DictWriter(csvfile, fieldnames=af_fieldnames)
                            writer.writerow(row)
            '''
            #print("now: files",files_count,dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), file,len(new_csv_files_dict), " "*10)
            for k,v in new_csv_files_dict.items():
                #print(v)
                #len_start = len(v)
                new_csv_files_dict = create_addr_dict_with_files(k,to_path,new_csv_files_dict)
                '''
                if len(new_csv_files_dict[k]) != len(v):
                    print(k, len(new_csv_files_dict[k]), len(v))
                    with open(k, 'a', newline='') as csvfile:
                        writer = csv.DictWriter(csvfile, fieldnames=af_fieldnames)
                        writer.writerows(v)
                '''
                with open(k, 'w', newline='') as csvfile:
                    writer = csv.DictWriter(csvfile, fieldnames=af_fieldnames)
                    writer.writeheader()
                    writer.writerows(v.values())
                #exit()
            #rename_file_path = os.path.sep.join([from_path,"_"+file])
            #os.rename(from_file_path, rename_file_path)
            delta = dt.datetime.now() - start_time
            print("now: ",files_count,dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), file, delta.total_seconds(),len(new_csv_files_dict), " "*20, end='\r')
            start_time = dt.datetime.now()
            file_del(from_file_path)
            #exit()
        files_count-=1

if __name__ == '__main__':
    print(__file__)
    to_path = "d:\\monero"
    #to_path = "/home/zdravek/projects/monero/address_csv_new/"
    print('start:',dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    from_path = "d:\\monero\\address_csv"
    #from_path = "/home/zdravek/projects/monero/address_csv"
    merge_files(from_path,to_path)
    #from_path = "/home/zdravek/projects/monero/address_csv_1"
    #merge_files(from_path,to_path)

    print('end:  ',dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),' '*10)