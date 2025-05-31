from config import *
from helper_mn import *

def get_transactions_from_block(block_no:int,debug=False):
    #print(b.__dict__.keys()) # dict_keys(['hash', 'height', 'timestamp', 'version', 'difficulty', 'nonce', 'prev_hash', 'reward', 'orphan', 'transactions', 'blob'])
    b = Daemon().block(height=block_no)
    if debug:
        for t in b.transactions:
            #print(t.__dict__.keys()) # dict_keys(['hash', 'fee', 'height', 'timestamp', 'key', 'blob', 'confirmations', 'output_indices', 'json', 'pubkeys', 'version'])
            print(t.__dict__)
    return b.transactions

def test_transactions_in_block(block_no:int,seed=rnd_seed(),debug=False):
    check = False
    for t in get_transactions_from_block(block_no):
        if debug: print('hash:\t',t.hash)
        #print(t.__dict__.keys()) #dict_keys(['hash', 'fee', 'height', 'timestamp', 'key', 'blob', 'confirmations', 'output_indices', 'json', 'pubkeys', 'version'])
        #print(t.json.keys()) #dict_keys(['version', 'unlock_time', 'vin', 'vout', 'extra', 'rct_signatures'])
        #print(t.json)
        extra = parseExtra(t.json['extra'])
        outputNum = len(t.json['vout'])
        pub = extra['pub']
        sec = seed.secret_view_key()
        if debug: print('pub:\t',pub,'sec:\t',sec)
        der = generate_key_derivation(pub, sec)
        if debug: print('der:\t',binascii.hexlify(der).decode())
        addrHex = base58.decode(str(seed.public_address()))
        spk = addrHex[2:66]
        for i in range(outputNum):
            pubkey = derive_public_key(der, i, spk)
            if pubkey == t.json['vout'][i]['target']['key']:
                print(block_no,t.hash,t.json['vout'][i])
                check = True
            else:
                print(block_no,t.hash,t.json['vout'][i]['target']['key'],pubkey)
    return check

def test_address_rows(af_rows,target_block,target_block_rows):
    af_new_rows={}
    for af_row in af_rows:
        #address_row address,hex,block,outputs
        if af_row['block'] == '': af_row['block']=-1
        if int(af_row['block'])+1==target_block:
            for target_row in target_block_rows:
                #time_print('now: ',[target_row['block_no'],target_row['output_no'],af_row['hex']])
                if check_output(target_row,af_row):
                    af_row['outputs']=target_row['outputs']+1
            af_row['block']=target_row['block_no']
        #af_new_rows.append(af_row)
        if af_row['address'] in af_new_rows.keys():
            if af_new_rows[af_row['address']] != af_row:
                print('overwrithed',af_new_rows[af_row['address']],'with',af_row)
        af_new_rows[af_row['address']] = af_row
        #print(af_row)
    #af_rows.line_num=0
    #print(list(af_rows),af_rows.__dict__)
    return sorted(af_new_rows.values(), key=lambda d: d['address'])

af_fieldnames = ['address','hex','block','outputs']

def test_loged_addreses(target_block = 0, adress_start = ''):
    target_block_rows = []
    for of in log_files('outputs')[:1]:
        of_path = path(of,['logs'])
        with open(of_path, newline='') as csv1file:
            of_rows = csv.DictReader(csv1file)
            for of_row in of_rows:
                #output_row block_no,transaction_hash,pub,output_no,output_key
                time_print('now: ',[of_path,str(of_rows.line_num),' '*60])
                if int(of_row['block_no']) < target_block:
                    pass
                elif int(of_row['block_no']) == target_block:
                    target_block_rows.append(of_row)
                else:
                    print()
                    for af_path in address_files(adress_start):
                        time_print('now: ',[str(target_block),af_path,' '*60])
                        #af_test_path = path(af,['test_logs'])
                        with open(af_path, newline='') as csv2file:
                            af_rows = csv.DictReader(csv2file)
                            #print(list(af_rows))
                            af_fieldnames = af_rows.fieldnames
                            af_new_rows=test_address_rows(af_rows,target_block,target_block_rows)
                        with open(af_path, 'w', newline='') as csv3file:
                            writer = csv.DictWriter(csv3file, fieldnames=af_fieldnames)
                            writer.writeheader()
                            writer.writerows(af_new_rows)
                        #print(of_rows)
                        #print(af_rows)
                    target_block+=1
                    target_block_rows=[]

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

first_out_dict = {
    'block_no': 0,
    'transaction_hash': "c88ce9783b4f11190d7b9c17a69c1c52200f9faaee8e98dd07e6811175177139",
    'pub': "7767aafcde9be00dcfd098715ebcf7f410daebc582fda69d24a28e9d0bc890d1",
    'output_no': 0,
    'output_key': "9b2e4c0281c0b02e7c53291a94d1d0cbff8883f8024f5142ee494ffbbd088071"
}

def test_rnd_addreses():
    target_block_rows = [first_out_dict]
    count=0
    while True:
        count = test_rnd_address(count,target_block_rows)

if __name__ == '__main__':
    print(__file__)
    #rnd_seed(True)
    #seed = Seed(test_mnemonic_seed)
    #print_seed(seed)
    #for block in test_blocks:
    #    print(block)
    #    test_transactions_in_block(block,seed)
    #while not test_transactions_in_block(1):
    #    pass
    #for addr in real_address:
    #    print(test_if_loged(addr))
    #c:/dev/python/.venv/Scripts/python.exe c:/dev/python/monero/proba.py
    print('start:',dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    test_loged_addreses(5)
    #test_rnd_addreses()
    print('end:  ',dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),' '*10)
