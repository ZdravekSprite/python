#pip install monero
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
        #print(b.__dict__)
        #print('get_block(self)',b.__dict__.keys())
        for k in ("hash", "height", "timestamp", "version", "difficulty", "nonce", "prev_hash", "reward", "orphan", "transactions", "blob"): setattr(self, k, getattr(b, k))

    def get_block_rpc(self):
        b = JSONRPCDaemon().get_block(height=self.height)
        #print(b)
        #print('get_block_rpc(self)',b.keys())
        # dict_keys(['blob', 'block_header', 'credits', 'json', 'miner_tx_hash', 'status', 'tx_hashes', 'top_hash', 'untrusted'])
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

    def variant_enc(self,hex):
        if len(hex)<3:
            return int(hex,16) if hex else 0
        elif int(hex,16) == 0:
            return 0
        else:
            #print(hex)
            bin_str = str(bin(int(hex,16)))[2:]
            #print(bin_str)
            drop_bits = ""
            xbit = ""
            for i in range(len(bin_str)):
                if i%8 != 0:
                    xbit+=bin_str[i]
                else:
                    drop_bits = xbit + drop_bits
                    xbit = ""
            drop_bits = xbit + drop_bits
            #print(drop_bits)
            varint = int(drop_bits,2)
            #print(varint)
            return varint

    def blob_slice(self,str:str,no:int):
        return (str[:no],str[no:])

    def parse_blob(self,debug=False):
        #print(self.__dict__.keys())
        #print(self.height)
        #print(self.transactions)
        #print(self.tx_hashes)
        #print(self.blob)
        blob_str = self.blob
        #print()

        if debug: print('verion:',self.version)

        blob_pre, blob_str = self.blob_slice(blob_str,2)
        if debug or self.variant_enc(blob_pre) != self.version[0]: print('major version (varint):    ',blob_pre,self.variant_enc(blob_pre),'verion:',self.version)
        blob_pre, blob_str = self.blob_slice(blob_str,2)
        if debug or self.variant_enc(blob_pre) != self.version[1]: print('minor version (varint):    ',blob_pre,self.variant_enc(blob_pre),'verion:',self.version)

        
        blob_pre, blob_str = self.blob_slice(blob_str,10)
        if debug or dt.fromtimestamp(self.variant_enc(blob_pre)) != self.timestamp:
            print('timestamp:',self.timestamp)
            print('timestamp (varint):        ',blob_pre,dt.fromtimestamp(self.variant_enc(blob_pre)))

        
        if int(self.prev_hash,16):
            blob_pre, blob_str = self.blob_slice(blob_str,64)
        else:
            blob_pre, blob_str = self.blob_slice(blob_str,56)
        if debug or int(blob_pre,16) != int(self.prev_hash,16):
            print('prev_hash:',self.prev_hash)
            print('prev ID:                   ',blob_pre)

        
        blob_pre, blob_str = self.blob_slice(blob_str,8)
        nonce = int(blob_pre[6:8]+blob_pre[4:6]+blob_pre[2:4]+blob_pre[0:2],16)
        if debug or nonce != self.nonce:
            print('nonce:',self.nonce)
            print('nonce (4 bytes):           ',blob_pre,nonce)

        
        blob_pre, blob_str = self.blob_slice(blob_str,2)
        if debug or self.variant_enc(blob_pre) != self.miner_tx_version:
            print('miner_tx_version:',self.miner_tx_version)
            print('miner TX version (varint): ',blob_pre,self.variant_enc(blob_pre))

        if self.height < 68: #256:
            blob_pre, blob_str = self.blob_slice(blob_str,6)
        elif self.height < 16324:
            blob_pre, blob_str = self.blob_slice(blob_str,8)
        elif self.height < 2097092:
            blob_pre, blob_str = self.blob_slice(blob_str,10)
        else:
            blob_pre, blob_str = self.blob_slice(blob_str,12)
            
        
        #if self.height >= 16324:
        #    blob_str = blob_str[2:]

        #print('unlock time (varint):      ',blob_pre,self.variant_enc(blob_pre))

        #print(self.vin)
        if self.height < 128: #256:
            height_with = 2
        elif self.height < 16384:
            height_with = 4
        elif self.height < 2097152:
            height_with = 6
        else:
            height_with = 8

        #print(blob_str)
        blob_pre, blob_str = self.blob_slice(blob_str,height_with)
        if debug or self.variant_enc(blob_pre) != self.height: print(self.height,'vin hight:                 ',blob_pre,self.variant_enc(blob_pre),hex(self.height),int(blob_pre,16),self.variant_enc(blob_pre[2:]))
        #if int(blob_pre,16) != self.height: print('vin hight:                 ',blob_pre,int(blob_pre,16),self.variant_enc(blob_pre),hex(self.height))
        #print(self.miner_tx_hash,self.blob.index(self.miner_tx_hash))
        #print(self.height,'vin hight:                 ',blob_pre,self.variant_enc(blob_pre),hex(self.height),int(blob_pre,16),self.variant_enc(blob_pre[2:]))

        #print(blob_str)
        blob_pre, blob_str = self.blob_slice(blob_str,2)
        if blob_str[:2] in ['01']:
            print('vin type (txin_gen):       ',blob_pre,self.vout[0])
            blob_pre, blob_str = self.blob_slice(blob_str,2)
            print('vin type (txin_gen):       ',blob_pre,self.vout[0])
        else:
            if debug: print('vin type (txin_gen):       ',blob_pre,self.vout[0])

        view_tag = '02'

        type = self.get_type(blob_str,view_tag,self.vout[0]['target'])

        if type == 0:
            blob_pre, blob_str = self.blob_slice(blob_str,2)
            if debug or blob_pre != view_tag:
                print('  type (txout_to_key):     ',blob_pre)
            type = self.get_type(blob_str,view_tag,self.vout[0]['target'])

        #print(type,blob_str[:180])
        blob_pre, blob_str = self.blob_slice(blob_str,type)
        if debug or self.variant_enc(blob_pre) != self.vout[0]['amount']:
            print(self.height,'  height (varint):         ',blob_pre,self.variant_enc(blob_pre),self.vout[0]['amount'])
            if debug or blob_pre[:2] in ['03']:
                print('  type (txout_to_key):             ',blob_pre[:2])
                print('  height (varint) next:            ',blob_pre[2:],self.variant_enc(blob_pre[2:]),self.vout[0]['amount'])
            else:
                print(self.height,'  height (varint) next:    ',blob_pre[2:],self.variant_enc(blob_pre[2:]),self.vout[0])

        blob_pre, blob_str = self.blob_slice(blob_str,2)
        if debug or blob_pre != view_tag: print('  type (txin_to_key):      ',blob_pre)
        blob_pre, blob_str = self.blob_slice(blob_str,64)
        if debug or blob_pre != self.get_target_key(self.vout[0]['target']): print('  key:                     ',blob_pre)

        #print('vout:',self.vout)
        vout_count = len(self.vout)-1
        
        #print('vout count:                ',vout_count)

        for vout in range(vout_count):
            do_print = False

            type = self.get_type(blob_str,view_tag,self.vout[vout+1]['target'])

            blob_pre, blob_str = self.blob_slice(blob_str,type)
            if debug or self.variant_enc(blob_pre) != self.vout[vout+1]['amount']:
                print(self.height,'  amount (varint):         ',blob_pre,self.variant_enc(blob_pre),self.vout[vout+1]['amount'])
                do_print = True
            blob_pre, blob_str = self.blob_slice(blob_str,2)
            if debug or blob_pre != view_tag:
                print('  type (txout_to_key):     ',blob_pre)
                do_print = True
            blob_pre, blob_str = self.blob_slice(blob_str,64)
            if debug or blob_pre != self.get_target_key(self.vout[vout+1]['target']):
                print('  key:                     ',blob_pre)
                do_print = True
            if debug or do_print: print(f'vout[{vout}]:',self.vout[vout+1])

        if len(self.extra)<128:
            blob_pre, blob_str = self.blob_slice(blob_str,2)
        else:
            blob_pre, blob_str = self.blob_slice(blob_str,4)
        #print(self.height,len(self.extra),len(blob_str),blob_pre, blob_str)
        if self.variant_enc(blob_pre) != len(self.extra):
        #if int(blob_pre,16) != len(self.extra):
            print(self.height,'extra size:                ',blob_pre,int(blob_pre,16),len(self.extra),blob_str)
        extra = [int(blob_str[2*i:2*i+2],16) for i in range(len(self.extra))]
        if extra != self.extra:
            print(self.height,len(blob_str),blob_pre, blob_str)
            print(self.height,'extra:',self.extra)
            print(self.height,'extra:                     ',extra,len(blob_str[:-2]))
        #if blob_str[-2:] != '00': print(self.height,'\tend:\t',blob_str[-2:])
        #print()

    def get_target_key(self,target):
        if 'key' in target.keys():
            target_key = target['key']
        else:
            target_key = target['tagged_key']['key']
        return target_key

    def get_type(self,blob_str,view_tag,target):
        target_key = self.get_target_key(target)
        type = blob_str.index(view_tag)
        if type%2:
            type = blob_str.index(view_tag,type+1)
        if blob_str[type+2:type+4] == view_tag: type+=2
        if blob_str[type+2:type+4] == view_tag: type+=2
        if blob_str[type+2:type+4] == view_tag: type+=2
        if blob_str[type+2:type+4] == view_tag: type+=2
        if target_key[:2] == view_tag:
            type-=2
            if target_key[2:4] == view_tag:
                type-=2
                if target_key[4:6] == view_tag:
                    type-=2
                    if target_key[6:8] == view_tag: type-=2
        return type

def print_keys(d:dict):
    for k,v in d.items():
        print(f'{k}:',v)


if __name__ == '__main__':
    print(__file__)
    #block_no = 13 #834112
    #blocks=[]
    for block_no in range(2688887,3400000):#range(3234439,3234440):
    #print_keys(get_block(block_no))
    #print_keys(get_block_rpc(block_no))
        if block_no%1000 == 0: print(block_no)
        #if block_no%10 == 0: print(block_no)
        #print(block_no)
        b = MyBlock(height=block_no)
        #blocks.append(b)
        #print_keys(b.__dict__)
        if block_no < 2688888:
            b.parse_blob()
        #print()
    #print(MyBlock(height=block_no).json)
    #print(blocks)
