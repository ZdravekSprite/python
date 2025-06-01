from helper_mn import *

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

def test_rnd_address(count,target_block_rows):
    seed = rnd_seed()
    af_path = path(f'{str(seed.public_address())[:4]}.csv',['address_csv'])
    rows_dict = dict_csv_dict_reader(af_path)
    #print('read',len(rows_dict.values()))
    if str(seed.public_address()) not in rows_dict.keys():
        count+=1
        if not count%100: time_print('now:  ',[str(count)])
        csv_row_dict = test_address(seed,target_block_rows)

        if not os.path.isfile(af_path):
            csv_dict_writer(af_path,[],af_fieldnames)
        #print(af_path,target_row,csv_row_dict)
        #rows_dict[str(seed.public_address())] = csv_row_dict
        #print('write',len(rows_dict.values()))
        csv_dict_adder(af_path,[csv_row_dict],af_fieldnames)
    return count

def test_rnd_addreses(blocks):
    target_block_rows = get_transactions(blocks)
    print(target_block_rows)
    count=0
    while True:
        count = test_rnd_address(count,target_block_rows)

def get_transactions(block_no:int,debug=False):
    target_block_rows = []
    for of in log_files('outputs'):
        of_path = path(of,['logs'])
        print(of_path)
        with open(of_path, newline='') as csv1file:
            of_rows = csv.DictReader(csv1file)
            for of_row in of_rows:
                #output_row block_no,transaction_hash,pub,output_no,output_key
                time_print('now: ',[of_path,str(of_rows.line_num),' '*60])
                if int(of_row['block_no']) <= block_no:
                    target_block_rows.append(of_row)
                else:
                    return target_block_rows

def test_if_addr_loged(addr):
    af_path = address_files(addr[:4])[0]
    addr_dict = dict_csv_dict_reader(af_path)
    if addr in addr_dict.keys():
        print(addr,af_path,addr_dict[addr])
        return (True,addr_dict)
    return (False,addr_dict)

if __name__ == '__main__':
    print(__file__)
    print('start:',dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    #test_rnd_addreses(5)
    seed = rnd_seed()
    addr = str(seed.public_address())
    print(test_if_addr_loged(addr)[0])
    print('end:  ',dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),' '*10)
