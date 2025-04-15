#pip install monero
#from monero.wallet import Wallet
from monero.seed import Seed
from monero.daemon import Daemon
from monero.block import Block
from config import test_seed

seed = Seed(phrase_or_hex=test_seed)
print("Address:", seed.public_address())
print()
daemon = Daemon()
print("Info:", daemon.info())
for h in daemon.headers(0,1):
    print("header:", h)
print()
for h in daemon.headers(912344,912345):
    print("header:", h)
print()
block = daemon.block(height=912345)
print("block:")
print(block.orphan)
print(block.transactions)
#print(block.blob)
def getnonce(hex):
    return int(hex[6:8]+hex[4:6]+hex[2:4]+hex[0:2],16)
def parse_blob(blob):
    print('major version (varint):    ',blob[0:2],int(blob[0:2],16))
    print('minor version (varint):    ',blob[2:4],int(blob[2:4],16))
    print('timestamp (varint):        ',blob[4:14],int(blob[4:14],16))
    print('prev ID:                   ',blob[14:78])
    print('nonce (4 bytes):           ',blob[78:86],getnonce(blob[78:86]))
    print('miner TX version (varint): ',blob[86:88],int(blob[86:88],16))
    print('unlock time (varint):      ',blob[88:94],int(blob[88:94],16))
    print('vin count:                 ',blob[94:96],int(blob[94:96],16))
    start = 96
    for vin in range(1):
        print(f'vin[{vin}]:')
        print('  type (txin_gen):     ',blob[start:start+2])
        print('  height (varint):     ',blob[start+2:start+8],int(blob[start+2:start+8],16))
        start = start+8
    print('vout count:                ',blob[start:start+2],int(blob[start:start+2],16))
    start = start+2
    for vout in range(4):
        print(f'vout[{vout}]:')
        type = blob[start:].index('02')
        print('  amount (varint):     ',blob[start:start+type],int(blob[start:start+type],16))
        print('  type (txin_to_key):  ',blob[start+type:start+type+2])
        print('  key:                 ',blob[start+type+2:start+type+66])
        start = start+type+66
    print('extra size: ',blob[start:start+2],int(blob[start:start+2],16))
    print('extra:      ',blob[start+2:-2])
    print('end:        ',blob[-2:])
    #print(blob)
    
parse_blob(block.blob)

'''
Block blob for block at height 912345:

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