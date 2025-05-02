import sys,os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import *

#pip install monero
from monero.daemon import Daemon
from monero.seed import Seed
#pip install requests
import requests

class myMonero:
    def __init__(self):
        self.daemon = Daemon()
    
    def get_transactions_from_block(self, block_no:int,debug=False):
        b = self.daemon.block(height=block_no)
        #print(b.__dict__.keys()) # dict_keys(['hash', 'height', 'timestamp', 'version', 'difficulty', 'nonce', 'prev_hash', 'reward', 'orphan', 'transactions', 'blob'])
        if debug:
            for t in b.transactions:
                #print(t.__dict__.keys()) # dict_keys(['hash', 'fee', 'height', 'timestamp', 'key', 'blob', 'confirmations', 'output_indices', 'json', 'pubkeys', 'version'])
                print('hash:              ',t.hash)
                t_json = t.json
                print('\tjson vin:        ',t_json['vin'])
                print('\tjson vout:') #       ',t_json['vout'])
                for vout in t_json['vout']:
                    #print('\t\t',vout)
                    print('\t\t',vout['target'],vout['amount'])
                print('\tjson extra:      ',t_json['extra'])
                if len(t.pubkeys): print('pubkeys:',t.pubkeys)
                if t.version != 1: print('version:',t.version)
        return b.transactions
    
    def show(self):
        print('myMonero')

def get_derivations(private_view_key,public_spend_key,outputNum,extra):
    json_post = {
        "private": private_view_key,
        "public": public_spend_key,
        "outputNum": outputNum,
        "extra": extra,
    }

    reqUrl = 'http://localhost:3000/transactions'
    response = requests.post(reqUrl, json=json_post)
    if response.status_code == 200:
        return response.json()['transactions']
    else:
        print(response.status_code)
        return []

def test_seed(debug=True):
    if debug:
        print('Test Mnemonic Seed:   ',test_mnemonic_seed)
        print('Test Private Spend Key:        ',test_private_spend_key)
        print('Test Private View Key:         ',test_private_view_key)
        print('Test Public Spend Key:         ',test_public_spend_key)
        print('Test Publice View Key:         ',test_public_view_key)
    #print(Seed().__dict__.keys()) # dict_keys(['phrase', 'hex', 'word_list', '_ed_pub_spend_key', '_ed_pub_view_key'])
    seed = Seed(test_mnemonic_seed)
    if debug: print_seed(seed)
    return seed

def rnd_seed(debug=False):
    #print(Seed().__dict__.keys()) # dict_keys(['phrase', 'hex', 'word_list', '_ed_pub_spend_key', '_ed_pub_view_key'])
    seed = Seed()
    seed.public_spend_key()
    seed.public_view_key()
    if debug: print_seed(seed)
    return seed

def print_seed(seed:Seed):
    print(seed.phrase)
    print(seed.secret_spend_key())
    print(seed.secret_view_key())
    print(seed.public_spend_key())
    print(seed.public_view_key())

def get_target_key(target):
    if 'key' in target.keys():
        target_key = target['key']
    else:
        target_key = target['tagged_key']['key']
    return target_key

def main_test():
    seed = test_seed()
    blocks = test_blocks
    check_trans_in_blocks(seed,blocks)

from monero.transaction.extra import ExtraParser
#print(test_res['transaction_data']['extra'])
#e = ExtraParser(test_res['transaction_data']['extra'])
#print(e.parse()['pubkeys'][0].hex())

def check_trans_in_blocks(seed:Seed,blocks:list):
    check = False
    for block_no in blocks:
        block_txs = myMonero().get_transactions_from_block(block_no)
        for tx in block_txs:
            print('\ntx hash:',tx.hash,'- block no:',tx.height)
            e = ExtraParser(tx.json['extra'])
            try:
                tx.pubkeys = [k.hex() for k in e.parse()['pubkeys']]
            except Exception as ex:
                print(ex)
            print('\ttx outputs:',tx.outputs())
            print('\ttx pubkeys:',tx.pubkeys)
            print(tx.json['extra'])
            '''
            derivations = get_derivations(seed.secret_view_key(),seed.public_spend_key(),len(tx.json['vout']),tx.json['extra'])
            #print(derivations)
            #print(tx.json['vout'])
            for i in range(len(tx.json['vout'])):
                key = get_target_key(tx.json['vout'][i]['target'])
                amount = tx.json['vout'][i]['amount']/1000000000000
                if key == derivations[i]:
                    print(key,amount,seed.phrase)
                    check = True
                else:
                    #print(key,derivations[i])
                    pass
            '''
    return check

if __name__ == '__main__':
    print(__file__)
    '''
    seed = rnd_seed()
    blocks = list(range(10))
    while not check_trans_in_blocks(seed,blocks):
        print(seed.phrase)
    '''
    seed = test_seed()
    blocks = test_block
    check_trans_in_blocks(seed,blocks)
    #print(seed.phrase)
 