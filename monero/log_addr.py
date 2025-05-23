from helper import *
from helper_mn import *

def log_addreses():
    fieldnames = ['address','hex','block','outputs'] #['hex','address','block']
    count=0
    for addr_file in [file for file in files_in_dir(path('',['logs'])) if file[:5] == 'addr_']:
        csv_file_path = path(addr_file,['logs'])
        with open(csv_file_path, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            count+=len(list(reader))
    while True:
        seed = rnd_seed()
        count+=1
        end = '\r' # '\x1b[1K\r'
        print('now:  ',dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),count, end=end)
        csv_row_dict = {
            #'time':dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'hex':seed.hex,
            'address':seed.public_address(),
            'block':'',
            'outputs':0
        }
        csv_file_path = path(f'addr_{str(seed.public_address())[:2]}.csv',['logs'])
        if not os.path.isfile(csv_file_path):
            csv_dict_writer(csv_file_path,[],fieldnames)
        csv_dict_adder(csv_file_path,[csv_row_dict],fieldnames)

def rearenge_addreses():
    count = 0
    #for addr_file in address_files():
    for addr_file in ['addreses_3378000.csv']:
        #csv_file_path = path(addr_file,['logs'])
        csv_file_path = path(addr_file)
        with open(csv_file_path, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            #new_fieldnames = ['address','hex','block','outputs']
            newlist = sorted(reader, key=lambda d: d['address'])
            for row in newlist:
                count+=1
                new_csv_file_path = path(f'address_{row['address'][:4]}.csv',['logs'])
                if not os.path.isfile(new_csv_file_path):
                    csv_dict_writer(new_csv_file_path,[],reader.fieldnames)
                '''
                new_row = {
                    'address':row['address'],
                    'hex':row['hex'],
                    'block':row['block'],
                    'outputs':0
                }
                '''
                csv_dict_adder(new_csv_file_path,[row],reader.fieldnames)
                print('now:  ',dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), reader.line_num, count, new_csv_file_path, ' '*10, end='\r')

def rearenge_addreses_x():
    csv_file_path = path("3378000.csv")
    new_csv_file_path = path("addreses_3378000.csv")
    with open(csv_file_path, newline='') as csvfile:
        reader = csv.reader(csvfile)
        new_fieldnames = ['address','hex','block','outputs']
        for row in reader:
            seed = Seed(" ".join(row[2:]))
            new_row = {
                'address':row[0],
                'hex':seed.hex,
                'block':3378000,
                'outputs':0
            }
            #csv_dict_adder(new_csv_file_path,[new_row],new_fieldnames)
            print('now:  ',dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), reader.line_num, new_csv_file_path, ' '*10, end='\r')

def test_if_real_found():
    for addr in real_address:
        print(addr)
        for af_path in address_files(addr[:4]):
            if addr in dict_csv_dict_reader(af_path).keys():
                print(addr,af_path,dict_csv_dict_reader(af_path)[addr])

def addr_count():
    count = 0
    for af_path in address_files():
        count += len(dict_csv_dict_reader(af_path).keys())
        time_print('now: ',[af_path,str(count)])
    print()
    return count

def max_count():
    count=1
    for i in range(24):
        count = count*(1626-i)
        print('total: ',len(str(count)),count)
    print()
    return count

if __name__ == '__main__':
    print(__file__)
    print('start:',dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    #log_addreses()
    #rearenge_addreses_x()
    #rearenge_addreses()
    #test_if_real_found()
    #addr_now = addr_count()
    max = max_count()
    #print('%:    ',(100*addr_now/max))
    print('end:  ',dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
