#pip install monero
#from monero.wallet import Wallet
from monero.seed import Seed
from monero.daemon import Daemon
from monero.block import Block
from config import *
from monero.backends.jsonrpc.daemon import JSONRPCDaemon
from helper_mn import *

def test_seed():
    seed = Seed(phrase_or_hex=test_seed)
    print("Address:", seed.public_address())
    print()

def getnonce(hex):
    return int(hex[6:8]+hex[4:6]+hex[2:4]+hex[0:2],16)

def test_daemon():
    daemon = Daemon()
    print("Info:", daemon.info())
    for h in daemon.headers(0,1):
        print("header:", h)

def test_block(height=912345):
    daemon = Daemon()
    print(daemon.headers(height))
    block = daemon.block(height=height)
    print("block:")
    print(block.orphan)
    print(block.transactions)
    #print(block.blob)
    parse_blob(block.blob,height==0)

'''
10010110 00000001        // Original inputs.
 0010110  0000001        // Drop continuation bits.
 0000001  0010110        // Convert to big-endian.
   00000010010110        // Concatenate.
 128 + 16 + 4 + 2 = 150  // Interpret as an unsigned 64-bit integer.
'''
def variant_enc(hex):
    if len(hex)<3:
        return int(hex,16)
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

def parse_blob(blob,first=False):
    print(blob)
    print('major version (varint):    ',blob[0:2],variant_enc(blob[0:2]))
    print('minor version (varint):    ',blob[2:4],variant_enc(blob[2:4]))
    print('timestamp (varint):        ',blob[4:14],variant_enc(blob[4:14]))
    if first:
        print('prvi',blob[14:])
    else:
        print('prev ID:                   ',blob[14:78])
        print('nonce (4 bytes):           ',blob[78:86],getnonce(blob[78:86]))
        print('miner TX version (varint): ',blob[86:88],variant_enc(blob[86:88]))
        print('unlock time (varint):      ',blob[88:94],variant_enc(blob[88:94]))
        vin_count = int(blob[94:96],16)
        print('vin count:                 ',blob[94:96],vin_count)
        start = 96
        for vin in range(vin_count):
            print(f'vin[{vin}]:')
            print('  type (txin_gen):     ',blob[start:start+2])
            print('  height (varint):     ',blob[start+2:start+8],variant_enc(blob[start+2:start+8]))
            start = start+8
        vout_count = int(blob[start:start+2],16)
        print('vout count:                ',blob[start:start+2],vout_count)
        start = start+2
        for vout in range(vout_count):
            print(f'vout[{vout}]:')
            type = blob[start:].index('02')
            print('  amount (varint):     ',blob[start:start+type],variant_enc(blob[start:start+type]))
            print('  type (txin_to_key):  ',blob[start+type:start+type+2])
            print('  key:                 ',blob[start+type+2:start+type+66])
            start = start+type+66
        print('extra size: ',blob[start:start+2],int(blob[start:start+2],16))
        print('extra:      ',blob[start+2:-2],len(blob[start+2:-2]))
        print('end:        ',blob[-2:])
    
    
'''
Block blob for block at height 912345:

0102f4bedfb405b61c58b2e0be53fad5ef9d9731a55e8a81d972b8d90ed07c04fd37ca6403ff786e0600000195d83701ffd9d73704ee84ddb42102378b043c1724c92c69d923d266fe86477d3a5ddd21145062e148c64c5767700880c0fc82aa020273733cbd6e6218bda671596462a4b062f95cfe5e1dbb5b990dacb30e827d02f280f092cbdd080247a5dab669770da69a860acde21616a119818e1a489bb3c4b1b6b3c50547bc0c80e08d84ddcb01021f7e4762b8b755e3e3c72b8610cc87b9bc25d1f0a87c0c816ebb952e4f8aff3d2b01fd0a778957f4f3103a838afda488c3cdadf2697b3d34ad71234282b2fad9100e02080000000bdfc2c16c00

major version (varint): 01
minor version (varint): 02
timestamp (varint): f4bedfb405
prev ID: b61c58b2e0be53fad5ef9d9731a55e8a81d972b8d90ed07c04fd37ca6403ff78
nonce (4 bytes): 6e060000
miner TX version (varint): 01
unlock time (varint): 95d837
vin count: 01
vin[0]:
  type (txin_gen): ff
  height (varint): d9d737
vout count: 04
vout[0]:
  amount (varint): ee84ddb421
  type (txin_to_key): 02
  key: 378b043c1724c92c69d923d266fe86477d3a5ddd21145062e148c64c57677008
vout[1]:
  amount (varint): 80c0fc82aa02
  type (txin_to_key): 02
  key: 73733cbd6e6218bda671596462a4b062f95cfe5e1dbb5b990dacb30e827d02f2
vout[2]:
  amount (varint): 80f092cbdd08
  type (txin_to_key): 02
  key: 47a5dab669770da69a860acde21616a119818e1a489bb3c4b1b6b3c50547bc0c
vout[3]:
  amount (varint): 80e08d84ddcb01
  type (txin_to_key): 02
  key: 1f7e4762b8b755e3e3c72b8610cc87b9bc25d1f0a87c0c816ebb952e4f8aff3d
extra size: 2b
extra: 01fd0a778957f4f3103a838afda488c3cdadf2697b3d34ad71234282b2fad9100e02080000000bdfc2c16c
end: 00
'''
from datetime import datetime as dt

def xmrchain_block(block_no:int):
    daemon = Daemon()
    #header = daemon.headers(block_no)[0]
    #print(header)
    block = daemon.block(height=block_no)
    print(block)
    #print(f'Block hash (height): {header['hash']} ({header['height']})')
    #print(f'Previous block: {header['prev_hash']}')
    #print(f'Next block: {daemon.headers(block_no+1)[0]['hash']}')
    #timestamp = header['timestamp']
    #print(f'Timestamp [UTC] (epoch): {dt.fromtimestamp(timestamp)} ({timestamp})\tAge [y:d:h:m:s]:	09:177:11:34:52\tΔ [h:m:s]:	00:01:53')
    #print(f'Major.minor version: {header['major_version']}.{header['minor_version']}\tBlock reward:	{header['reward']/1000000000000}\tBlock size [kB]:	{header['block_size']/1024}')
    #print(f'nonce: {header['nonce']}\tTotal fees:	0.032625\tNo of txs: {header['num_txes']}')
    #print(f'PoW hash: f4b6bb2d240114077f3e31c07aab264426e9f9b83e7a5e028bee3f3202000000\tDifficulty: {header['difficulty']}')
    #b = xmrBlock(header['height'],block.transactions,header['prev_hash'],timestamp,header['nonce'],header['reward'])
    #print(b.hash)
    
import hashlib

class xmrBlock:
    def __init__(self, block_number, transactions, previous_hash, timestamp, nonce, reward):
        self.block_number = block_number
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.nonce = nonce
        self.reward = reward
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        data = str(self.block_number) + str(self.transactions) + self.previous_hash + str(self.timestamp) + str(self.nonce) + str(self.reward)
        return hashlib.sha256(data.encode()).hexdigest()

def xmrchain_block_json(block_no:int):
    daemon = JSONRPCDaemon()
    block = daemon.get_block(height=block_no)
    print(block['json'])
    pass

if __name__ == '__main__':
    print(__file__)
    #variant_enc('f4bedfb405')
    #test_daemon()
    #for x in range(1,10):
    #    test_block(x)
    #xmrchain_block(795523)
    #test_block(795523)
    #xmrchain_block_json(795523)
    seed = Seed(test_mnemonic_seed)
    print(seed.public_address())
    decode = base58.decode(str(seed.public_address()))
    print(decode)
    net = decode[:2]
    public_spend_key = decode[2:66]
    public_view_key = decode[66:130]
    print(net,public_spend_key,public_view_key)
    print('12',seed.public_spend_key(),seed.public_view_key())
