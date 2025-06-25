import os
import datetime as dt
import csv

af_fieldnames = ['address','hex','block','outputs']

def de_x00(addr):
    while True:
        if addr[0]=='\00':
            addr = addr[1:]
        else:
            return addr

if __name__ == '__main__':
    print(__file__)
    from_dict_path = "c:\\monero\\address_csv_2"
    from_files = next(os.walk(from_dict_path), (None, None, []))[2]
    print('start:',dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    for file in from_files:
        path_to_dict = os.path.sep.join([from_dict_path,file])
        print("now:  ", path_to_dict, " "*20, end='\r')
        with open(path_to_dict, newline='') as csvfile:
            reader = csv.DictReader(csvfile, fieldnames=af_fieldnames)
            for row in reader:
                if row['address'][0]=='\00':
                    print("now:  ", de_x00(row['address']), " "*20, end='\r')
    print()
    print('end:  ',dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),' '*20)