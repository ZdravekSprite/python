from config import *
from proba import *

def print_R2L():
    print("\nstart")
    print("\naccount")
    print("seed",test_mnemonic_seed)
    print("hex",test_hexadecimal_seed)
    print("secret_spend_key",test_private_spend_key)
    print("secret_view_key",test_private_view_key)
    print("public_spend_key",test_public_spend_key)
    print("public_view_key",test_public_view_key)
    print("public_address",test_public_address)
    print("\nblock")
    print("extra",test_extra)
    print("pub",test_pub,parseExtra(test_extra)['pub'])
    print("\ntransaction")
    print("tx_hash",test_tx_hash)
    print("public_tx_key",test_public_tx_key)
    print("derived_key",test_derived_key,binascii.hexlify(generate_key_derivation(test_pub, test_private_view_key)).decode())
    print("\noutputs")
    pubkey = derive_public_key(binascii.unhexlify(test_derived_key.encode()), 0, test_public_spend_key, True)
    print("(output) pub key 0",test_output_0,pubkey)
    #print("key image 0",key_image_0)
    #print("output 1",test_output_1)
    #print("key image 1",key_image_1)
    #print("output 2",test_output_2)
    #print("key image 2",key_image_2)
    print("end")

def print_L2R():
    print("end")
    print("output 0",test_output_0)
    print("start")

if __name__ == '__main__':
    print(__file__)
    print_R2L()
    print_L2R()
