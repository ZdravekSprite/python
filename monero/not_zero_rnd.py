import os
import datetime as dt
import threading
import binascii
import varint

from config import first_out_dict, real_address
from helper_file import path, csv_dict_writer, csv_dict_adder
from helper import time_print

#pip install monero
from monero.seed import Seed
from monero import ed25519
from monero import base58
from monero.keccak import keccak_256

af_fieldnames = ['address','hex','block','outputs']

def rnd_seed(debug=False):
    #print(Seed().__dict__.keys()) # dict_keys(['phrase', 'hex', 'word_list', '_ed_pub_spend_key', '_ed_pub_view_key'])
    seed = Seed()
    seed.public_spend_key()
    seed.public_view_key()
    return seed

def generate_key_derivation(pub, sec, debug=False):
    svk = binascii.unhexlify(sec)
    svk_2 = ed25519.scalar_add(svk, svk)
    svk_4 = ed25519.scalar_add(svk_2, svk_2)
    svk_8 = ed25519.scalar_add(svk_4, svk_4)
    shared_secret = ed25519.scalarmult(svk_8, binascii.unhexlify(pub))
    return shared_secret

def derive_public_key(der, i, spk,debug=False):
    shared_secret = der
    psk = binascii.unhexlify(spk)

    hsdata = b"".join(
        [
            shared_secret,
            varint.encode(i),
        ]
    )
    Hs_ur = keccak_256(hsdata).digest()
    Hs = ed25519.scalar_reduce(Hs_ur)
    k = ed25519.edwards_add(
        ed25519.scalarmult_B(Hs),
        psk,
    )
    return binascii.hexlify(k).decode()

def check_output(output_row,address_row):
    #output_row block_no,transaction_hash,pub,output_no,output_key
    #address_row address,hex,block,outputs
    #addr = Seed(address_row['hex'])
    pub = output_row['pub']
    sec = address_row['svk']
    der = generate_key_derivation(pub, sec)
    #spk = base58.decode(address_row['address'])[2:66]
    spk = address_row['psk']
    #print(spk,address_row['psk'])
    pubkey = derive_public_key(der, int(output_row['output_no']), spk)
    del address_row['svk']
    del address_row['psk']
    
    if address_row['address'] in real_address:
        print('\nreal',address_row)
        #r_fieldnames = ['address','hex']
        r_fieldnames = address_row.keys()
        real_row = address_row
        csv_file_path = path(f'real.csv',['logs'])
        csv_dict_adder(csv_file_path,[real_row],r_fieldnames)

    if pubkey == output_row['output_key']:
        print(output_row,address_row)
        c_fieldnames = ['block_no','transaction_hash','pub','output_no','output_key','address','hex']
        confirm_row = output_row
        confirm_row['address']=address_row['address']
        confirm_row['hex']=address_row['hex']
        csv_file_path = path(f'confirmed.csv',['logs'])
        csv_dict_adder(csv_file_path,[confirm_row],c_fieldnames)

    return pubkey == output_row['output_key']

def test_address(csv_row_dict,target_block_rows):
    for target_row in target_block_rows:
        if check_output(target_row,csv_row_dict):
            csv_row_dict['outputs']=target_row['outputs']+1
    csv_row_dict['block']=target_row['block_no']
    return csv_row_dict

def test_rnd_address_fast(count,target_block_rows,start_time):
    seed = rnd_seed()
    af_path = path(f'{str(seed.public_address())[:4]}.csv'.lower(),['address_csv'])
    #if str(seed.public_address()) not in rows_dict.keys():
    if True:
        count+=1
        if not count%100:
            now_time = dt.datetime.now()
            delta = now_time - start_time
            time_print('now:  ',[str(count),str(int(count//delta.total_seconds()))])
        csv_row_dict = {
            'hex':seed.hex,
            'address':str(seed.public_address()),
            'svk':str(seed.secret_view_key()),
            'psk':str(seed.public_spend_key()),
            'block':-1,
            'outputs':0
        }
        csv_row_dict = test_address(csv_row_dict,target_block_rows)

        if not os.path.isfile(af_path):
            csv_dict_writer(af_path,[],af_fieldnames)
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