#pip install monero
from monero.daemon import Daemon
from monero.seed import Seed
from monero import ed25519
from monero import base58
from monero.keccak import keccak_256
import binascii
import varint
from config import *
from helper import *

def print_seed(seed:Seed):
    print(seed.phrase)
    print(seed.hex)
    print(seed.secret_spend_key())
    print(seed.secret_view_key())
    print(seed.public_spend_key())
    print(seed.public_view_key())
    print(seed.public_address())

def rnd_seed(debug=False):
    #print(Seed().__dict__.keys()) # dict_keys(['phrase', 'hex', 'word_list', '_ed_pub_spend_key', '_ed_pub_view_key'])
    seed = Seed()
    seed.public_spend_key()
    seed.public_view_key()
    if debug: print_seed(seed)
    return seed

def parseExtra(bin,debug=False):
    extra = {
        'pub': False,
        'paymentId': False
    }
    if bin[0] == 1: #pubkey is tag 1
        extra['pub'] = base58._binToHex(bin[1: 33]) #pubkey is 32 bytes
        if debug: print(bin,len(bin))
        if len(bin)>35 and (bin[33] == 2 and bin[35] == 0 or bin[35] == 1):
            extra['paymentId'] = base58._binToHex(bin[36:36 + bin[34] - 1])
    elif bin[0] == 2:
        if debug:
            print(bin,len(bin))
            print(bin[-33])
            print(bin[-32:])
        if bin[2] == 0 or bin[2] == 1:
            extra['paymentId'] = base58._binToHex(bin[3: 3 + bin[1] - 1])
        #second byte of nonce is nonce payload length; payload length + nonce tag byte + payload length byte should be the location of the pubkey tag
        if bin[2 + bin[1]] == 1:
            offset = 2 + bin[1]
            extra['pub'] = base58._binToHex(bin[offset + 1: offset + 1 + 32])
        elif bin[-33] == 1:
            extra['pub'] = base58._binToHex(bin[-32:])
    else:
        if debug: print(extra,bin)
    return extra

def generate_key_derivation(pub, sec, debug=False):
    svk = binascii.unhexlify(sec)
    if debug:
        print('private_view_key:')
        print('svk:               ',sec,svk)
    svk_2 = ed25519.scalar_add(svk, svk)
    if debug: print('svk2:              ',binascii.hexlify(svk_2).decode(),svk_2)
    svk_4 = ed25519.scalar_add(svk_2, svk_2)
    if debug: print('svk4:              ',binascii.hexlify(svk_4).decode(),svk_4)
    svk_8 = ed25519.scalar_add(svk_4, svk_4)
    if debug:
        print('svk8:              ',binascii.hexlify(svk_8).decode(),svk_8)
        print('pub:               ',pub,binascii.unhexlify(pub))
    shared_secret = ed25519.scalarmult(svk_8, binascii.unhexlify(pub))
    return shared_secret

def derive_public_key(der, i, spk,debug=False):
    shared_secret = der
    if debug:
        print('shared_secret:            ',binascii.hexlify(shared_secret).decode(),shared_secret)
        print('keccak_256(shared_secret):',keccak_256(shared_secret).hexdigest())
    psk = binascii.unhexlify(spk)

    hsdata = b"".join(
        [
            shared_secret,
            varint.encode(i),
        ]
    )
    if debug:
        print('hsdata:                   ',binascii.hexlify(hsdata).decode(),hsdata)
        print('keccak_256(hsdata):       ',keccak_256(hsdata).hexdigest())
    Hs_ur = keccak_256(hsdata).digest()
    if debug:
        print('Hs_ur:                    ',binascii.hexlify(Hs_ur).decode(),Hs_ur)
    Hs = ed25519.scalar_reduce(Hs_ur)
    if debug:
        print('Hs:                       ',binascii.hexlify(Hs).decode(),Hs)
        print(format(int(binascii.hexlify(Hs).decode(),16), '0>42b'))
        print(base58._hexToBin(binascii.hexlify(Hs).decode()))
        print('ed25519.scalarmult_B(Hs): ',binascii.hexlify(ed25519.scalarmult_B(Hs)).decode(),ed25519.scalarmult_B(Hs))
        print(format(int(binascii.hexlify(ed25519.scalarmult_B(Hs)).decode(),16), '0>42b'))
        print(base58._hexToBin(binascii.hexlify(ed25519.scalarmult_B(Hs)).decode()))
    k = ed25519.edwards_add(
        ed25519.scalarmult_B(Hs),
        psk,
    )
    if debug:
        print('k:                        ',binascii.hexlify(k).decode(),k)
        #print(':                         ',ed25519.nacl.bindings.crypto_box_beforenm(k,psk))
    return binascii.hexlify(k).decode()

def check_output(output_row,address_row,debug=False):
    #output_row block_no,transaction_hash,pub,output_no,output_key
    #address_row address,hex,block,outputs
    #seed = Seed(test_mnemonic_seed)
    #print_seed(seed)
    addr = Seed(address_row['hex'])
    pub = output_row['pub']
    if debug: print('pub: ',pub,test_pub)
    sec = addr.secret_view_key()
    if debug: print('sec: ',sec,test_sec)
    der = generate_key_derivation(pub, sec)
    if debug: print('der: ',der,test_der)
    spk = base58.decode(address_row['address'])[2:66]
    if debug: print(spk)
    pubkey = derive_public_key(der, int(output_row['output_no']), spk)
    if debug: print(pubkey,output_row['output_key'])

    if pubkey == output_row['output_key']:
        print(output_row,address_row)
        c_fieldnames = ['block_no','transaction_hash','pub','output_no','output_key','address','hex']
        confirm_row = output_row
        confirm_row['address']=address_row['address']
        confirm_row['hex']=address_row['hex']
        csv_file_path = path(f'confirmed.csv',['logs'])
        if not os.path.isfile(csv_file_path):
            csv_dict_writer(csv_file_path,[],c_fieldnames)
        csv_dict_adder(csv_file_path,[confirm_row],c_fieldnames)

    return pubkey == output_row['output_key']

def confirm_check():
    confirm_path = path(f'confirmed.csv',['logs'])
    with open(confirm_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            addr = Seed(row['hex'])
            pub = row['pub']
            sec = addr.secret_view_key()
            der = generate_key_derivation(pub, sec)
            spk = base58.decode(row['address'])[2:66]
            pubkey = derive_public_key(der, int(row['output_no']), spk)

            if pubkey == row['output_key']:
                print(row)
                c_fieldnames = ['block_no','transaction_hash','pub','output_no','output_key','address','hex']
                confirm_row = row
                csv_file_path = path(f'confirmed_new.csv',['logs'])
                if not os.path.isfile(csv_file_path):
                    csv_dict_writer(csv_file_path,[],c_fieldnames)
                csv_dict_adder(csv_file_path,[confirm_row],c_fieldnames)

if __name__ == '__main__':
    print(__file__)
    #print("derived_key, output index, public spend key -> derive_public_key(derived_key, output_index, public_spend_key) -> public output key")
    #pubkey = derive_public_key(binascii.unhexlify(test_derived_key.encode()), 0, test_public_spend_key,True)
    #print("(output) pub key 0:       ",test_output_0,pubkey)
    for af_path in address_files():
        time_print('now: ',[af_path,' '*60])
        #af_test_path = path(af,['test_logs'])
        with open(af_path, newline='') as csv2file:
            af_rows = csv.DictReader(csv2file)
            for row in af_rows:
                if int(row['outputs'])>0: print(row)
