from monero.daemon import Daemon
from monero.backends.jsonrpc.daemon import JSONRPCDaemon
import json
from datetime import datetime as dt

class MyBlock():
    def __init__(self, height:int):
        self.height = height
        self.get_block()
        self.get_block_rpc()
    
    def __str__(self):
        return f'block:\t\t{self.height}\n\t\t{self.hash}\ntimestamp:\t{self.timestamp}'

    def get_block(self):
        b = Daemon().block(height=self.height)
        #print('get_block(self)',b.__dict__.keys())
        for k in ("hash", "height", "timestamp", "version", "difficulty", "nonce", "prev_hash", "reward", "orphan", "transactions", "blob"): setattr(self, k, getattr(b, k))
        #print(b)

    def get_block_rpc(self):
        b = JSONRPCDaemon().get_block(height=self.height)
        #print('get_block_rpc(self)',b.keys())
        # dict_keys(['blob', 'block_header', 'credits', 'json', 'miner_tx_hash', 'status', 'top_hash', 'untrusted'])
        for k in b.keys():
            # 'blob'
            if k == 'blob':
                if self.blob != b['blob']: print('blob error')
            # 'credits', 'miner_tx_hash', 'status', 'top_hash', 'untrusted'
            elif k in ['credits', 'miner_tx_hash', 'status', 'top_hash', 'untrusted', 'tx_hashes']:
                setattr(self, k, b[k])
            # 'block_header'
            elif k == 'block_header':
                self.set_attr_from_header(b['block_header'])
            # 'json'
            elif k == 'json':
                self.set_attr_from_json(json.loads(b['json']))
            else:
                print('k?',k,b[k])
    
    def set_attr_from_header(self, block_header):
        # 'block_size', 'block_weight', 'cumulative_difficulty', 'cumulative_difficulty_top64', 'depth', 'difficulty', 'difficulty_top64', 'hash', 'height', 'long_term_weight',
        # 'major_version', 'miner_tx_hash', 'minor_version', 'nonce', 'num_txes', 'orphan_status', 'pow_hash', 'prev_hash', 'reward', 'timestamp', 'wide_cumulative_difficulty',
        # 'wide_difficulty'
        #print(self.__dict__.keys())
        #print('\tblock_header\n\t',block_header.keys(),'\n',block_header)
        setattr(self, 'block_size', block_header['block_size'])
        self.if_not_equal(block_header['block_size'],block_header['block_weight'],'block_weight')
        self.if_not_equal(block_header['cumulative_difficulty'],int(block_header['wide_cumulative_difficulty'],16),'wide_cumulative_difficulty')
        self.if_not_equal(block_header['cumulative_difficulty_top64'],0)
        self.if_not_equal(block_header['difficulty_top64'],0)
        self.if_not_equal(block_header['difficulty'],int(block_header['wide_difficulty'],16),'wide_difficulty')
        self.if_not_equal(self.difficulty,block_header['difficulty'],'difficulty')
        self.if_not_equal(self.hash,block_header['hash'],'hash')
        self.if_not_equal(self.height,block_header['height'],'height')
        #self.if_not_equal(block_header['block_size'],block_header['long_term_weight'],'long_term_weight')
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
        #print(self.__dict__.keys())
        #print('\tjson\n\t',block_json.keys(),'\n',block_json)
        self.if_not_equal(self.version,(block_json['major_version'],block_json['minor_version']))
        self.if_not_equal(self.timestamp,dt.fromtimestamp(block_json['timestamp']),'timestamp')
        self.if_not_equal(self.prev_hash,block_json['prev_id'],'prev_id')
        self.if_not_equal(self.nonce,block_json['nonce'],'nonce')
        #setattr(self, 'miner_tx', block_json['miner_tx'])
        self.set_attr_from_miner_tx(block_json['miner_tx'])
        if 'tx_hashes' in self.__dict__.keys():
            self.if_not_equal(self.tx_hashes,block_json['tx_hashes'],'tx_hashes')
        else:
            setattr(self, 'tx_hashes', block_json['tx_hashes'])
        for k in block_json.keys():
            if k not in ['major_version', 'minor_version', 'timestamp', 'prev_id', 'nonce', 'miner_tx', 'tx_hashes']:
                print(k)

    def set_attr_from_miner_tx(self, block_miner_tx):
        #print('miner_tx',block_miner_tx)
        # 'version', 'unlock_time', 'vin', 'vout', 'extra', 'signatures', 'rct_signatures'
        #print(self.height,block_miner_tx.keys())
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
        #print(sum([t['amount'] for t in block_miner_tx['vout']]))
        #if len(block_miner_tx['extra']) != 33: print(self.height,'extra:',len(block_miner_tx['extra']))
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

def print_keys(d:dict):
    for k,v in d.items():
        print(f'{k}:',v)

if __name__ == '__main__':
    print(__file__)
    #block_no = 13 #834112
    #blocks=[]
    for block_no in range(834110,835440):
    #print_keys(get_block(block_no))
    #print_keys(get_block_rpc(block_no))
        if block_no%1000 == 0: print(block_no)
        b = MyBlock(height=block_no)
        #blocks.append(b)
        #print_keys(b.__dict__)
        #print()
    #print(MyBlock(height=block_no).json)
    #print(blocks)
