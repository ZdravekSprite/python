import sys,os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import *

#pip install monero
from monero.base58 import _hexToBin as hextobin
from monero import ed25519
import binascii

#var der = generate_key_derivation(pub, sec)

def generate_key_derivation(pub, sec):
    svk = binascii.unhexlify(sec)
    svk_2 = ed25519.scalar_add(svk, svk)
    svk_4 = ed25519.scalar_add(svk_2, svk_2)
    svk_8 = ed25519.scalar_add(svk_4, svk_4)
    shared_secret = ed25519.scalarmult(svk_8, binascii.unhexlify(pub))
    return shared_secret

if __name__ == '__main__':
    print(__file__)
    shared_secret = generate_key_derivation(test_pub, test_sec)
    print(binascii.hexlify(shared_secret).decode(),test_derived_key)
