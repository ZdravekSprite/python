from ..config import *
from words25 import words25
from hexseed import mn_decode
from private import cn_fast_hash,sc_reduce32
from public import publickey

import base58 as _b58

'''
def calc_address(A: bytes, B: bytes):
    """
    Args:
        A: bytes; public view key
        B: bytes; public spend key 
    """

    data = bytearray([18]) + A + B
    checksum = keccak_256(data).digest()[:4]
    return base58.encode((data + checksum).hex())
'''

def encode_addr(version, publicSpendKey, publicViewKey):
    '''Given address version and public spend and view keys, derive address.'''
    data = version + publicSpendKey + publicViewKey
    checksum = cn_fast_hash(data)
    return _b58.encode(data + checksum[0:8])
 
def test():
    public_spend_key = publickey(test_private_spend_key)
    public_view_key = publickey(test_private_view_key)
    monero_public_address = encode_addr("12",public_spend_key,public_view_key)
    print('Mnemonic Seed:',test_mnemonic_seed)
    print('25 words seed:',words25(" ".join(test_mnemonic_seed.split(" ")[:24])))
    print('Hexadecimal Seed:',test_hexadecimal_seed)
    print('mn_decode:       ',mn_decode(test_mnemonic_seed))
    print('Private View Key:         ',test_private_view_key)
    print('cn_fast_hash:             ',cn_fast_hash(test_hexadecimal_seed))
    print('sc_reduce32(cn_fast_hash):',sc_reduce32(cn_fast_hash(test_hexadecimal_seed)))
    print('Public Spend Key:',test_public_spend_key)
    print('publickey(spend):',publickey(test_private_spend_key))
    print('Public View Key: ',test_public_view_key)
    print('publickey(view): ',publickey(test_private_view_key))
    print('Public Address:',test_public_address)
    print('encode_addr:   ',monero_public_address)

if __name__ == '__main__':
    print(__file__)
    print(bytearray([18]),'12')
