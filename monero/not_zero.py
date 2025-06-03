import os
import csv
import datetime as dt
from slow import *
from helper_hex import *
from helper_file import *
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

class AddressSlow():
    def __init__(self, hex_=''):
        self.hex_ = hex_ if len(hex_)==64 else generate_random_hex()
    
    def check_slow(
            self,
            pub = "7767aafcde9be00dcfd098715ebcf7f410daebc582fda69d24a28e9d0bc890d1",
            no = 0,
            key = "9b2e4c0281c0b02e7c53291a94d1d0cbff8883f8024f5142ee494ffbbd088071"
        ):
        hex_ = self.hex_
        sec = secret_view_key(hex_)
        der = generate_key_derivation(pub, sec)
        spk = base58.decode(public_address(hex_))[2:66]
        pubkey = derive_public_key(der, no, spk)
        return pubkey == key

    def public_address(self):
        hex_ = self.hex_
        netbyte = (18, 53, 24)[0]
        data = "{:x}{:s}{:s}".format(
            netbyte, public_spend_key(hex_), public_view_key(hex_)
        )
        k256 = keccak.new(digest_bits=256)
        k256.update(unhexlify(data))
        checksum = k256.hexdigest()
        return str(base58.encode(data + checksum[0:8]))

    def address_file(self):
        return self.public_address()[:4].lower()+".csv"

def rnd_check(to_path, debug = False):
    addr = AddressSlow()
    file_path = os.path.sep.join([to_path]+[addr.address_file()])
    the_file_path = os.path.sep.join([to_path]+["zero.csv"])
    real_path = os.path.sep.join([to_path]+["real.csv"])
    data = csv_reader(file_path)
    notin = True
    hex_ = addr.hex_
    if addr.public_address() in real_address:
        csv_adder(real_path,[[addr.public_address(),addr.hex_]])
    if [addr.hex_] not in data:
        check = addr.check_slow()
        if check:
            csv_writer(the_file_path,[[addr.hex_]])
        else:
            csv_adder(file_path,[[addr.hex_]])
    else:
        check = False
        notin = False
    if debug: print(hex_,check,file_path,notin)
    return check

if __name__ == '__main__':
    print(__file__)
    to_path = "c:\\monero\\not_zero"
    print('start:',dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    #from_path = "c:\\monero\\address_csv"
    #format(from_path,to_path)
    '''
    test_addr = AddressSlow(test_address_row['hex'])
    print(
        test_address_row['hex'],
        test_addr.check_slow(
            test_output_row['pub'],
            test_output_row['output_no'],
            test_output_row['output_key']
            ),
        test_addr.public_address(),
        test_addr.address_file()
        )
    '''
    count = 0
    temp_count = 0
    start_time = dt.datetime.now()
    while not rnd_check(to_path):
        count+=1
        temp_count+=1
        if not count%100:
            now_time = dt.datetime.now()
            delta = now_time - start_time
            print('now',dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), count,int(temp_count//delta.total_seconds()), " "*10, end='\r')
            temp_count = 0
            start_time = dt.datetime.now()
    print()
    print('end:  ',dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),' '*10)