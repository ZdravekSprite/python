import os
import csv
import datetime as dt
from slow import *
from helper_hex import *
from monero import base58
from config import *

def format(from_path,to_path):
    count=0
    from_ = next(os.walk(from_path), (None, None, []))[2]
    for file in from_:
        path_from = os.path.sep.join([from_path,file])
        path_to = os.path.sep.join([to_path,file])
        if not os.path.isfile(path_to):
            with open(path_to, 'w') as fp:
                pass
        hexs = []
        with open(path_to, newline='') as to_reader:
            reader = csv.reader(to_reader)
            for row in reader:
                if row[0] and row[0] not in hexs:
                    hexs.append([row[0]])
                    count+=1
        with open(path_from, newline='') as from_reader:
            reader = csv.DictReader(from_reader)
            for row in reader:
                if row['hex'] and row['hex'] not in hexs:
                    hexs.append([row['hex']])
                    count+=1
        with open(path_to, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            writer.writerows(hexs)
        print("now: ",dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), file, str(count), " "*10, end='\r')
    print()

def check_slow(
        hex_,
        pub = "7767aafcde9be00dcfd098715ebcf7f410daebc582fda69d24a28e9d0bc890d1",
        no = 0,
        key = "9b2e4c0281c0b02e7c53291a94d1d0cbff8883f8024f5142ee494ffbbd088071"
    ):
    sec = secret_view_key(hex_)
    der = generate_key_derivation(pub, sec)
    spk = base58.decode(public_address(hex_))[2:66]
    pubkey = derive_public_key(der, no, spk)
    return pubkey == key

def check_fast(
        unhexlify_hex,
        unhexlify_pub = b'wg\xaa\xfc\xde\x9b\xe0\r\xcf\xd0\x98q^\xbc\xf7\xf4\x10\xda\xeb\xc5\x82\xfd\xa6\x9d$\xa2\x8e\x9d\x0b\xc8\x90\xd1',
        variant_no = b'\x00',
        unhexlify_key = b'\x9b.L\x02\x81\xc0\xb0.|S)\x1a\x94\xd1\xd0\xcb\xff\x88\x83\xf8\x02OQB\xeeIO\xfb\xbd\x08\x80q'
    ):
    '''
    unhexlify_hex = unhexlify(hex_)
    unhexlify_pub = unhexlify(pub)
    print(unhexlify_pub)
    variant_no = variant_encode(no)
    print(variant_no)
    unhexlify_key = unhexlify(key)
    print(unhexlify_key)
    '''

    b = scalar_reduce(unhexlify_hex)
    svk = scalar_reduce_keccak_256(b)
    svk_2 = scalar_add(svk, svk)
    svk_4 = scalar_add(svk_2, svk_2)
    svk_8 = scalar_add(svk_4, svk_4)
    der = scalarmult(svk_8, unhexlify_pub)
    spk = scalarmult_B(scalar_reduce(unhexlify_hex))
    hsdata = b"".join([der,variant_no])
    Hs = scalar_reduce_keccak_256(hsdata)

    k = edwards_add(
        scalarmult_B(Hs),
        spk
    )
    return k == unhexlify_key

def rnd_check(debug = False):
    hex_ = generate_random_hex()
    check = check_fast(unhexlify(hex_))
    addr = public_address(hex_)
    if debug: print(hex_,check,addr)
    return check

if __name__ == '__main__':
    print(__file__)
    to_path = "c:\\monero\\not_zero"
    print('start:',dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    #from_path = "c:\\monero\\address_csv"
    #format(from_path,to_path)
    '''
    print(
        test_address_row['hex'],
        check_fast(
            unhexlify(test_address_row['hex']),
            unhexlify(test_output_row['pub']),
            variant_encode(test_output_row['output_no']),
            unhexlify(test_output_row['output_key']),
            ))
    '''
    rnd_check(True)
    print('end:  ',dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),' '*10)