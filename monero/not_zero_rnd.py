import os
import datetime as dt
import threading
from config import first_out_dict
from helper_mn import rnd_seed, check_output
from helper_file import path, csv_dict_writer, csv_dict_adder
from helper import time_print

af_fieldnames = ['address','hex','block','outputs']

def test_address(seed,target_block_rows):
    csv_row_dict = {
        'hex':seed.hex,
        'address':str(seed.public_address()),
        'block':'-1',
        'outputs':0
    }
    for target_row in target_block_rows:
        #print(target_row,csv_row_dict)
        if check_output(target_row,csv_row_dict):
            csv_row_dict['outputs']=target_row['outputs']+1
    csv_row_dict['block']=target_row['block_no']
    return csv_row_dict

def test_rnd_address_fast(count,target_block_rows,start_time):
    seed = rnd_seed()
    af_path = path(f'{str(seed.public_address())[:4]}.csv'.lower(),['address_csv'])
    #rows_dict = dict_csv_dict_reader(af_path,af_fieldnames)
    #print('read',len(rows_dict.values()))
    #if str(seed.public_address()) not in rows_dict.keys():
    if True:
        count+=1
        if not count%100:
            now_time = dt.datetime.now()
            delta = now_time - start_time
            time_print('now:  ',[str(count),str(int(count//delta.total_seconds()))])
        csv_row_dict = test_address(seed,target_block_rows)

        if not os.path.isfile(af_path):
            csv_dict_writer(af_path,[],af_fieldnames)
        #print(af_path,target_row,csv_row_dict)
        #rows_dict[str(seed.public_address())] = csv_row_dict
        #print('write',len(rows_dict.values()))
        csv_dict_adder(af_path,[csv_row_dict],af_fieldnames)
    return count

def test_rnd_addreses(blocks=0, debuge = False):
    if blocks == 0:
        target_block_rows = [first_out_dict]
    else:
        return False
        #target_block_rows = get_transactions(blocks)
    if debuge: print(target_block_rows)
    count=0
    start_time = dt.datetime.now()
    while not done:
        #count = test_rnd_address(count,target_block_rows,start_time)
        count = test_rnd_address_fast(count,target_block_rows,start_time)

if __name__ == '__main__':
    print(__file__)
    print('start:',dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    done = False
    threat_count = int(input('How much? '))
    for i in range(threat_count):
        threading.Thread(target=test_rnd_addreses, daemon=True).start()
    input('Pres enter to quit\n')
    done = True

    print('end:  ',dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),' '*10)