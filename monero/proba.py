from config import *
from helper_mn import *
from helper import *

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

def test_if_loged(address:str):
    print(address)
    for f in log_files(f'addr_{address[:2]}'):
        time_print('now: ',[f])
        csv = csv_dict_reader(path(f,['logs']))
        for row in csv:
            #address_row address,hex,block,outputs
            if row['address'] == address: return True

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
    print('start:',dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    target_block = 1
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
                    for af in log_files('address_'):
                        af_path = path(af,['logs'])
                        time_print('now: ',[af_path,' '*60])
                        #af_test_path = path(af,['test_logs'])
                        with open(af_path, newline='') as csv2file:
                            af_rows = csv.DictReader(csv2file)
                            #print(list(af_rows))
                            af_new_rows=[]
                            af_fieldnames = af_rows.fieldnames
                            for af_row in af_rows:
                                #address_row address,hex,block,outputs
                                if af_row['block'] == '': af_row['block']=0
                                if int(af_row['block'])+1==target_block:
                                    for target_row in target_block_rows:
                                        #time_print('now: ',[target_row['block_no'],target_row['output_no'],af_row['hex']])
                                        if check_output(target_row,af_row):
                                            print(target_row,af_row)
                                            c_fieldnames = ['block_no','transaction_hash','pub','output_no','output_key','address','hex']
                                            confirm_row = target_row
                                            confirm_row['address']=af_row['address']
                                            confirm_row['hex']=af_row['hex']
                                            csv_file_path = path(f'confirmed.csv',['logs'])
                                            if not os.path.isfile(csv_file_path):
                                                csv_dict_writer(csv_file_path,[],c_fieldnames)
                                            csv_dict_adder(csv_file_path,[confirm_row],c_fieldnames)
                                            af_row['outputs']=target_row['outputs']+1
                                    af_row['block']=target_row['block_no']
                                af_new_rows.append(af_row)
                                #print(af_row)
                            #af_rows.line_num=0
                            #print(list(af_rows),af_rows.__dict__)
                        with open(af_path, 'w', newline='') as csv3file:
                            writer = csv.DictWriter(csv3file, fieldnames=af_fieldnames)
                            writer.writeheader()
                            writer.writerows(af_new_rows)
                        #print(of_rows)
                        #print(af_rows)
                    target_block+=1
                    target_block_rows=[]
    print('end:  ',dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),' '*10)
