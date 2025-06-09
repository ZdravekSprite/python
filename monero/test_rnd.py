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

def test_rnd_address(count,target_block_rows,start_time):
    seed = rnd_seed()
    af_path = path(f'{str(seed.public_address())[:4]}.csv'.lower(),['address_csv'])
    rows_dict = dict_csv_dict_reader(af_path,af_fieldnames)
    #print('read',len(rows_dict.values()))
    if str(seed.public_address()) not in rows_dict.keys():
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
        target_block_rows = get_transactions(blocks)
    if debuge: print(target_block_rows)
    count=0
    start_time = dt.datetime.now()
    while not done:
        #count = test_rnd_address(count,target_block_rows,start_time)
        count = test_rnd_address_fast(count,target_block_rows,start_time)

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

def add_row_to_dict(dict_,row_):
    if row_['address'] in dict_.keys():
        if dict_[row_['address']] != row_:
            '''
            print('DIFFER:',dict_[row_['address']]['hex'],dict_[row_['address']]['address'],
                  'old:',dict_[row_['address']]['block'],dict_[row_['address']]['outputs'],
                  'new:',row_['block'],row_['outputs'],
                  " "*10, end='\r')
            '''
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
        dict_[row_['address']] = row_
    return dict_

def dict_write(dict_path,dict_):
    with open(dict_path, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=af_fieldnames)
        writer.writeheader()
        writer.writerows(dict_.values())

def create_addr_dict(dict_path,csv_dict):
    with open(dict_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile, fieldnames=af_fieldnames)
        for row in reader:
            if row['address'] != 'address': csv_dict = add_row_to_dict(csv_dict, row)
    return csv_dict

def merge_dict(from_path,to_path):
    from_files = next(os.walk(from_path), (None, None, []))[2]
    count=0
    start_time = dt.datetime.now()
    for file in from_files:
        
        path_to_dict = os.path.sep.join([to_path,'address_csv',file])
        if not os.path.isfile(path_to_dict):
            with open(path_to_dict.lower(), 'w', newline='') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=af_fieldnames)
                writer.writeheader()
        
        csv_dict = {}
        csv_dict = create_addr_dict(path_to_dict,csv_dict)
        delta_count = len(csv_dict)

        path_from_dict = os.path.sep.join([from_path,file])
        csv_dict = create_addr_dict(path_from_dict,csv_dict)
        dict_write(path_to_dict,csv_dict)

        delta_count = len(csv_dict)-delta_count
        count+=len(csv_dict)
        now_time = dt.datetime.now()
        delta = now_time - start_time
        print("now: ",dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), file, count, int(delta_count//delta.total_seconds()), " "*10, end='\r')
        start_time = dt.datetime.now()
    print()

if __name__ == '__main__':
    print(__file__)
    from_dict_path = "c:\\monero\\address_csv_1"
    to_path = "c:\\monero"
    print('start:',dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    #merge_dict(from_dict_path,to_path)

    import threading
    done = False
    threat_count = int(input('How much? '))
    for i in range(threat_count):
        threading.Thread(target=test_rnd_addreses, daemon=True).start()
    input('Pres enter to quit\n')
    done = True

    #test_rnd_addreses()
    #seed = rnd_seed()
    #addr = str(seed.public_address())
    #print(test_if_addr_loged(addr)[0])
    print('end:  ',dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),' '*10)
