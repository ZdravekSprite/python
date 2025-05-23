from config import *
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
    for block_no in range(100000,200000): #3402968 2900
        time_print('now:  ',[str(block_no)])
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
            time_print('now:  ',[str(reader.line_num), block, new_csv_file_path])

def test_check_address_from_files():
    for file in log_files('outputs'):
        file_path = path(file,['logs'])
        with open(file_path, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                #output_row block_no,transaction_hash,pub,output_no,output_key
                b_o = f"{row['block_no']}.{row['output_no']}"
                time_print('now:  ',[str(reader.line_num), b_o])
                if check_output(row,test_address_row):
                    print(row,test_address_row)

def test_check_address_from_chan(start_block,debug=False):
    for block_no in range(start_block,1000000):
        time_print('now:  ',[str(block_no)])
        for t in get_transactions_from_block(block_no):
            outputNum = len(t.json['vout'])
            if outputNum:
                if debug: print(block_no,t.__dict__)
                pub = parseExtra(t.json['extra'],debug)['pub']
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
                    if check_output(csv_row_dict,test_address_row,debug):
                        print(csv_row_dict,test_address_row)
                        fieldnames = ['block_no','transaction_hash','pub','output_no','output_key','address','hex']
                        csv_row_dict['address']=test_address_row['address']
                        csv_row_dict['hex']=test_address_row['hex']
                        csv_file_path = path(f'confirmed.csv',['logs'])
                    else:
                        fieldnames = ['block_no','transaction_hash','pub','output_no','output_key']
                        file_no='{:0>4}'.format(int(block_no)//10000)
                        csv_file_path = path(f'outputs{file_no}.csv',['logs'])
                    if not os.path.isfile(csv_file_path):
                        csv_dict_writer(csv_file_path,[],fieldnames)
                    if not debug: csv_dict_adder(csv_file_path,[csv_row_dict],fieldnames)

def out_count():
    count = 0
    for of in log_files('outputs'):
        of_path = path(of,['logs'])
        count += len(csv_dict_reader(of_path))
        time_print('now: ',[of_path,str(count)])
    print()
    return count

if __name__ == '__main__':
    print(__file__)
    print('start:',dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    #log_outputs()
    #test_check_address_from_files()
    test_check_address_from_chan(681099)
    #print(check_output(test_output_row,test_address_row,True))
    print('end:  ',dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
