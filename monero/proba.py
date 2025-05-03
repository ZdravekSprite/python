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

