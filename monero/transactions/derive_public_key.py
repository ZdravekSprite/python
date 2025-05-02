import sys,os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import *

import binascii
import varint
from monero.keccak import keccak_256
from monero import ed25519

#var pubkey = derive_public_key(der, i, spk)

def derive_public_key(der, i, spk):
    shared_secret = der
    psk = binascii.unhexlify(spk)

    hsdata = b"".join(
        [
            shared_secret,
            varint.encode(i),
        ]
    )
    Hs_ur = keccak_256(hsdata).digest()
    Hs = ed25519.scalar_reduce(Hs_ur)
    k = ed25519.edwards_add(
        ed25519.scalarmult_B(Hs),
        psk,
    )
    return binascii.hexlify(k).decode()


if __name__ == '__main__':
    print(__file__)
    for i in range(6):
        k = derive_public_key(binascii.unhexlify(test_derived_key.encode()), i, test_public_spend_key.encode())
        print(k)
