import dependencies.ed25519_changed as ed25519
from dependencies.util import *
from config import *

#pip install pycryptodome
from Crypto.Hash import keccak
def cn_fast_hash(str):
    k = keccak.new(digest_bits=256)
    k.update(bytearray.fromhex(str))
    return k.hexdigest()

def calc_key_image(a: bytes, b: bytes, R: bytes, i:int) -> bytes:
    """Calculate key image for input 

    Args:
        a: bytes; Private view key
        b: bytes; Private spend key 
        R: bytes; Transaction public key (rG) of refferenced output transaction. Stored in field extra[1:33]).hex(). 
        i: int; output index of refferenced output

    Returns:
        Key image : string
    """
    
    # x = H_s(aR) + b
    aR = ed25519.encodepoint(ed25519.scalarmult(ed25519.decodepoint(R), ed25519.decodeint(a)))
    aR =  ed25519.encodepoint(ed25519.scalarmult(ed25519.decodepoint(aR),  8 )) # There is a mathematical reason for this...
    aR += bytes([i])

    #Hs = sc_reduce32(keccak_256(aR).digest())
    Hs = sc_reduce32(keccak.new(data=aR,digest_bits=256).digest())

    x = int.from_bytes(Hs, byteorder='little') + int.from_bytes(b, byteorder='little')
    x = x % ed25519.l
    x = x.to_bytes(32, 'little')    

    Hp = hashToPointCN(ed25519.publickey(x))
    return ed25519.encodepoint(ed25519.scalarmult(Hp, ed25519.decodeint(x)))

if __name__ == '__main__':
    print(__file__)
    a=test_b_private_view_key #Private view key
    b=test_b_private_spend_key #Private spend key
    R=test_b_public_tx_key #Transaction public key (rG) of refferenced output transaction. Stored in field extra[1:33]).hex(). 
    i=0   #output index of refferenced output
    print(calc_key_image(a, b, R, i))
