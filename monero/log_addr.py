from helper import *
from helper_mn import *

def get_transactions_from_block(block_no:int,debug=False):
    #print(b.__dict__.keys()) # dict_keys(['hash', 'height', 'timestamp', 'version', 'difficulty', 'nonce', 'prev_hash', 'reward', 'orphan', 'transactions', 'blob'])
    b = Daemon().block(height=block_no)
    if debug:
        for t in b.transactions:
            #print(t.__dict__.keys()) # dict_keys(['hash', 'fee', 'height', 'timestamp', 'key', 'blob', 'confirmations', 'output_indices', 'json', 'pubkeys', 'version'])
            print(t.__dict__)
    return b.transactions

def log_outputs():
    fieldnames = ['block_no','transaction_hash','pub','output_no','output_key'] # ['time','block_no','transaction_hash','pub','output_no','output_key']
    #csv_file_path = path('test.csv')
    #csv_dict_writer(csv_file_path,[],fieldnames)
    for block_no in range(78050,100000): #3402968 2900
        end = '\r' # '\x1b[1K\r'
        print('now:  ',dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), block_no, end=end)
        for t in get_transactions_from_block(block_no):
            pub = parseExtra(t.json['extra'])['pub']
            outputNum = len(t.json['vout'])
            outputs = t.json['vout']
            for i in range(outputNum):
                csv_row_dict = {
                    #'time':dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    'block_no':block_no,
                    'transaction_hash':t.hash,
                    'pub':pub,
                    'output_no':i,
                    'output_key':outputs[i]['target']['key']
                }
                file_no='{:0>4}'.format(int(block_no)//10000)
                csv_file_path = path(f'outputs{file_no}.csv',['logs'])
                if not os.path.isfile(csv_file_path):
                    csv_dict_writer(csv_file_path,[],fieldnames)
                csv_dict_adder(csv_file_path,[csv_row_dict],fieldnames)

def removekey(d, key):
    r = dict(d)
    del r[key]
    return r

def rearenge_outputs():
    csv_file_path = path('test.csv')
    with open(csv_file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        new_fieldnames = reader.fieldnames[1:]
        for row in reader:
            block=row['block_no']
            file_no='{:0>4}'.format(int(block)//10000)
            new_csv_file_path = path(f'outputs{file_no}.csv',['logs'])
            if not os.path.isfile(new_csv_file_path):
                csv_dict_writer(new_csv_file_path,[],new_fieldnames)
            new_row = removekey(row, 'time')
            csv_dict_adder(new_csv_file_path,[new_row],new_fieldnames)
            print('now:  ',dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), reader.line_num, block, new_csv_file_path, end='\r')

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
    #for addr_file in log_files('addr_'):
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
            csv_dict_adder(new_csv_file_path,[new_row],new_fieldnames)
            print('now:  ',dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), reader.line_num, new_csv_file_path, ' '*10, end='\r')

if __name__ == '__main__':
    print(__file__)
    print('start:',dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    #log_outputs()
    #log_addreses()
    #rearenge_addreses_x()
    rearenge_addreses()
    print('end:  ',dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
