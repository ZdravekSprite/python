#pip install monero
from monero.daemon import Daemon
from monero.backends.jsonrpc.daemon import JSONRPCDaemon
import json
from datetime import datetime as dt
from config import *
#pip install requests
import requests

class MyBlock():
    def __init__(self, height:int):
        self.height = height
        self.get_block()
        self.get_block_rpc()
    
    def __str__(self):
        return f'block:\t\t{self.height}\n\t\t{self.hash}\ntimestamp:\t{self.timestamp}'

    def get_block(self):
        b = Daemon().block(height=self.height)
        for k in ("hash", "height", "timestamp", "version", "difficulty", "nonce", "prev_hash", "reward", "orphan", "transactions", "blob"): setattr(self, k, getattr(b, k))

    def get_block_rpc(self):
        b = JSONRPCDaemon().get_block(height=self.height)
        for k in b.keys():
            if k == 'blob':
                if self.blob != b['blob']: print('blob error')
            elif k in ['credits', 'miner_tx_hash', 'status', 'top_hash', 'untrusted', 'tx_hashes']:
                setattr(self, k, b[k])
            elif k == 'block_header':
                self.set_attr_from_header(b['block_header'])
            elif k == 'json':
                self.set_attr_from_json(json.loads(b['json']))
            else:
                print('k?',k,b[k])
    
    def get_transaction(self,tx_tash):
        ts = JSONRPCDaemon().get_transactions([tx_tash],True)
        #print(ts.keys()) #dict_keys(['credits', 'status', 'top_hash', 'txs', 'txs_as_hex', 'txs_as_json', 'untrusted'])
        return ts['txs'][0]
    
    def show_transactions(self):
        print(self.transactions)
    
    def set_attr_from_header(self, block_header):
        setattr(self, 'block_size', block_header['block_size'])
        self.if_not_equal(block_header['block_size'],block_header['block_weight'],'block_weight')
        self.if_not_equal(block_header['cumulative_difficulty'],int(block_header['wide_cumulative_difficulty'],16),'wide_cumulative_difficulty')
        self.if_not_equal(block_header['cumulative_difficulty_top64'],0)
        self.if_not_equal(block_header['difficulty_top64'],0)
        self.if_not_equal(block_header['difficulty'],int(block_header['wide_difficulty'],16),'wide_difficulty')
        self.if_not_equal(self.difficulty,block_header['difficulty'],'difficulty')
        self.if_not_equal(self.hash,block_header['hash'],'hash')
        self.if_not_equal(self.height,block_header['height'],'height')
        setattr(self, 'long_term_weight', block_header['long_term_weight'])
        self.if_not_equal(self.version,(block_header['major_version'],block_header['minor_version']),'version')
        if 'miner_tx_hash' in self.__dict__.keys():
            self.if_not_equal(self.miner_tx_hash,block_header['miner_tx_hash'],'miner_tx_hash')
        else:
            setattr(self, 'miner_tx_hash', block_header['miner_tx_hash'])
        self.if_not_equal(self.nonce,block_header['nonce'],'nonce')
        setattr(self, 'num_txes', block_header['num_txes'])
        self.if_not_equal(self.orphan,block_header['orphan_status'],'orphan_status')
        self.if_not_equal(block_header['pow_hash'],'','pow_hash')
        self.if_not_equal(self.prev_hash,block_header['prev_hash'])
        self.if_not_equal(self.reward*1000000000000,block_header['reward'],'reward')
        self.if_not_equal(self.timestamp,dt.fromtimestamp(block_header['timestamp']),'timestamp')

    def set_attr_from_json(self, block_json):
        self.if_not_equal(self.version,(block_json['major_version'],block_json['minor_version']))
        self.if_not_equal(self.timestamp,dt.fromtimestamp(block_json['timestamp']),'timestamp')
        self.if_not_equal(self.prev_hash,block_json['prev_id'],'prev_id')
        self.if_not_equal(self.nonce,block_json['nonce'],'nonce')
        self.set_attr_from_miner_tx(block_json['miner_tx'])
        if 'tx_hashes' in self.__dict__.keys():
            self.if_not_equal(self.tx_hashes,block_json['tx_hashes'],'tx_hashes')
        else:
            setattr(self, 'tx_hashes', block_json['tx_hashes'])
        for k in block_json.keys():
            if k not in ['major_version', 'minor_version', 'timestamp', 'prev_id', 'nonce', 'miner_tx', 'tx_hashes']:
                print(k)

    def set_attr_from_miner_tx(self, block_miner_tx):
        if len(block_miner_tx.keys()) != 6: print(self.height,'keys:',len(block_miner_tx.keys()))
        setattr(self, 'miner_tx_version', block_miner_tx['version'])
        self.if_not_equal(self.height+60,block_miner_tx['unlock_time'],'unlock_time')
        if len(block_miner_tx['vin']) != 1 or len(block_miner_tx['vin'][0]['gen']) != 1 or block_miner_tx['vin'][0]['gen']['height'] != self.height:
            print(self.height,'vin:',len(block_miner_tx['vin']))
            setattr(self, 'vin', block_miner_tx['vin'])
            print(block_miner_tx['vin'])
        setattr(self, 'vout', block_miner_tx['vout'])
        if sum([t['amount'] for t in block_miner_tx['vout']]) != self.reward*1000000000000:
            print(block_miner_tx['vout'])
        setattr(self, 'extra', block_miner_tx['extra'])
        if 'signatures' in block_miner_tx.keys() and len(block_miner_tx['signatures']) != 0:
            print(self.height,'signatures:',len(block_miner_tx['signatures']))
            setattr(self, 'signatures', block_miner_tx['signatures'])
        if 'rct_signatures' in block_miner_tx.keys():
            if len(block_miner_tx['rct_signatures'].keys()) != 1 or block_miner_tx['rct_signatures']['type'] != 0:
                print(self.height,'rct_signatures:',len(block_miner_tx['rct_signatures']), block_miner_tx['rct_signatures'])
                setattr(self, 'rct_signatures', block_miner_tx['rct_signatures'])

    def if_not_equal(self,a,b,attr=''):
        if a != b: print(self.height,attr,':',a,'!=',b)

    def variant_enc(self,hex):
        if len(hex)<3:
            return int(hex,16) if hex else 0
        elif int(hex,16) == 0:
            return 0
        else:
            bin_str = str(bin(int(hex,16)))[2:]
            drop_bits = ""
            xbit = ""
            for i in range(len(bin_str)):
                if i%8 != 0:
                    xbit+=bin_str[i]
                else:
                    drop_bits = xbit + drop_bits
                    xbit = ""
            drop_bits = xbit + drop_bits
            varint = int(drop_bits,2)
            return varint

    def blob_slice(self,str:str,no:int):
        return (str[:no],str[no:])

def get_target_key(target):
    if 'key' in target.keys():
        target_key = target['key']
    else:
        target_key = target['tagged_key']['key']
    return target_key

if __name__ == '__main__':
    print(__file__)
    block_no = 13 #834112
    b = MyBlock(height=block_no)
    #print(b.extra)
    for t in test_transactions:
        tx = b.get_transaction(t)
        tx_json = json.loads(tx['as_json'])
        json_post = {
            "private": test_private_view_key,
            "public": test_public_spend_key,
            "outputNum": len(tx_json['vout']),
            "extra": tx_json['extra'],
        }

        reqUrl = 'http://localhost:3000/transactions'
        response = requests.post(reqUrl, json=json_post)
        print(response.status_code)
        res = response.json()
        print(tx['block_height'],t)
        public_txs = res['transactions']
        for i in range(len(tx_json['vout'])):
            if public_txs[str(i)] == get_target_key(tx_json['vout'][i]['target']):
                print(tx_json['vout'][i])
            else:
                print(tx_json['vout'][i],public_txs[str(i)])
