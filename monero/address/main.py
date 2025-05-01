from ..config import *
from hexseed import mn_decode
from private import cn_fast_hash,sc_reduce32
from public import publickey
from address import encode_addr

def test(test_seed,test_address):
    print('Mnemonic Seed:     ',test_seed)
    hexadecimal_seed = mn_decode(test_seed)
    #print('hexadecimal_seed:  ',hexadecimal_seed)
    private_spend_key = hexadecimal_seed
    #print('private_spend_key:',private_spend_key)
    public_spend_key = publickey(private_spend_key)
    #print('public_spend_key:',public_spend_key)
    private_view_key = sc_reduce32(cn_fast_hash(hexadecimal_seed))
    #print('private_view_key:',private_view_key)
    public_view_key = publickey(private_view_key)
    #print('public_view_key: ',public_view_key)
    monero_public_address = encode_addr("12",public_spend_key,public_view_key)
    print('Public Address:    ',test_address)
    if test_address != monero_public_address:
        print('encode_addr:   ',monero_public_address)

def test_show():
    print('Mnemonic Seed:     ',test_mnemonic_seed)
    print()
    print('Hexadecimal Seed:  ',test_hexadecimal_seed)
    hexadecimal_seed = mn_decode(test_mnemonic_seed)
    print('hexadecimal_seed:  ',hexadecimal_seed)
    print()
    private_spend_key = hexadecimal_seed
    print('Private Spend Key: ',test_private_spend_key)
    print('private_spend_key:',private_spend_key)
    print()
    public_spend_key = publickey(private_spend_key)
    print('Public Spend Key:',test_public_spend_key)
    print('public_spend_key:',public_spend_key)
    print()
    private_view_key = sc_reduce32(cn_fast_hash(hexadecimal_seed))
    print('Private View Key: ',test_private_view_key)
    print('private_view_key:',private_view_key)
    print()
    public_view_key = publickey(private_view_key)
    print('Public View Key: ',test_public_view_key)
    print('public_view_key: ',public_view_key)
    print()
    monero_public_address = encode_addr("12",public_spend_key,public_view_key)
    print('Public Address:',test_public_address)
    print('encode_addr:   ',monero_public_address)

def print_all(test_seed):
    print('Mnemonic Seed:     ',test_seed)
    hexadecimal_seed = mn_decode(test_mnemonic_seed)
    print('Hexadecimal Seed:  ',hexadecimal_seed)
    private_spend_key = hexadecimal_seed
    print('Private Spend Key: ',private_spend_key)
    public_spend_key = publickey(private_spend_key)
    print('Public Spend Key:  ',public_spend_key)
    private_view_key = sc_reduce32(cn_fast_hash(hexadecimal_seed))
    print('Private View Key:  ',private_view_key)
    public_view_key = publickey(private_view_key)
    print('Public View Key:   ',public_view_key)
    monero_public_address = encode_addr("12",public_spend_key,public_view_key)
    print('Public Address:    ',monero_public_address)

if __name__ == '__main__':
    print(__file__)
    #'''
    for el in test_list:
        test_seed =" ".join(el[2])
        #print(test_seed)
        test_address = el[0]
        #print(test_address)
        #print(el[1])
        #print_all(test_seed)
        try:
            test(test_seed,test_address)
            #pass
        except Exception as ex:
            print(ex)
#'''

    #print_all(test_seed)
