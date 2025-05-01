#pip install monero
from monero.seed import Seed
from monero.daemon import Daemon
from monero import ed25519
from monero import base58
from monero.keccak import keccak_256
import binascii
import varint
from config import *

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

def get_transactions_from_block(block_no:int,debug=False):
    #print(b.__dict__.keys()) # dict_keys(['hash', 'height', 'timestamp', 'version', 'difficulty', 'nonce', 'prev_hash', 'reward', 'orphan', 'transactions', 'blob'])
    b = Daemon().block(height=block_no)
    if debug:
            for t in b.transactions:
                #print(t.__dict__.keys()) # dict_keys(['hash', 'fee', 'height', 'timestamp', 'key', 'blob', 'confirmations', 'output_indices', 'json', 'pubkeys', 'version'])
                print(t.__dict__)
    return b.transactions

def parseExtra(bin):
    extra = {
        'pub': False,
        'paymentId': False
    }
    if bin[0] == 1: #pubkey is tag 1
        extra['pub'] = base58._binToHex(bin[1: 33]) #pubkey is 32 bytes
        #print(bin,len(bin))
        if len(bin)>33 and (bin[33] == 2 and bin[35] == 0 or bin[35] == 1):
            extra['paymentId'] = base58._binToHex(bin[36:36 + bin[34] - 1])
    elif bin[0] == 2:
        if bin[2] == 0 or bin[2] == 1:
            extra['paymentId'] = base58._binToHex(bin[3: 3 + bin[1] - 1])
        #second byte of nonce is nonce payload length; payload length + nonce tag byte + payload length byte should be the location of the pubkey tag
        if bin[2 + bin[1]] == 1:
            offset = 2 + bin[1]
            extra['pub'] = base58._binToHex(bin[offset + 1: offset + 1 + 32])
    return extra

def generate_key_derivation(pub, sec):
    svk = binascii.unhexlify(sec)
    svk_2 = ed25519.scalar_add(svk, svk)
    svk_4 = ed25519.scalar_add(svk_2, svk_2)
    svk_8 = ed25519.scalar_add(svk_4, svk_4)
    shared_secret = ed25519.scalarmult(svk_8, binascii.unhexlify(pub))
    return shared_secret

def derive_public_key(der, i, spk):
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

if __name__ == '__main__':
    print(__file__)
    #rnd_seed(True)
    #seed = Seed(test_mnemonic_seed)
    #print_seed(seed)
    #for block in test_blocks:
    #    print(block)
    #    test_transactions_in_block(block,seed)
    while not test_transactions_in_block(1):
        pass

