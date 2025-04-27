from config import *
from seed import Seed
import binascii
import operator as _oper

int2byte = _oper.methodcaller("to_bytes", 1, "big")

#pip install pycryptodome
from Crypto.Hash import keccak
def cn_fast_hash(str):
    k = keccak.new(digest_bits=256)
    k.update(bytearray.fromhex(str))
    return k.hexdigest()

l = 2 ** 252 + 27742317777372353535851937790883648493
b = 256

def sc_reduce32(key):
    return int("%x" % int(int.from_bytes(int(key,16).to_bytes(32, 'little'), 'big') % l),16).to_bytes(32, byteorder='little').hex()

def expmod(b,e,m):
    if e == 0: return 1
    t = expmod(b,e//2,m)**2 % m
    if e & 1: t = (t*b) % m
    return t

def edwards(P,Q):
    q = 2**255 - 19
    def inv(x):
        return expmod(x,q-2,q)
    d = -121665 * inv(121666)
    x1,y1 = P
    x2,y2 = Q
    x3 = (x1*y2+x2*y1) * inv(1+d*x1*x2*y1*y2)
    y3 = (y1*y2+x1*x2) * inv(1-d*x1*x2*y1*y2)
    return [x3 % q,y3 % q]

def scalarmult(P,e):
    if e == 0: return [0,1]
    Q = scalarmult(P,e//2)
    Q = edwards(Q,Q)
    if e & 1: Q = edwards(Q,P)
    return Q

def encodepoint(P):
    x,y = P
    bits = [(y >> i) & 1 for i in range(b-1)] + [x & 1]
    return b''.join([int2byte(sum([bits[i * 8 + j] << j for j in range(8)])) for i in range(b//8)])

def publickey(sk):
    sk = binascii.unhexlify(sk)
    try:
        a = sum(2**i * ((ord(chr(sk[int(i//8)])) >> (i%8)) & 1) for i in range(0,b))
    except Exception as ex:
        print(ex,sk,len(sk))
    B = [15112221349535400772501151409588531511454012693041857206046113283949847762202, 46316835694926478169428394003475163141307993866256225615783033603165251855960]
    A = scalarmult(B,a)
    #print('encodep',encodepoint(A))
    #end = binascii.hexlify(encodepoint(A)).decode()
    #print('encodep',binascii.unhexlify(end.encode("utf-8")))
    return binascii.hexlify(encodepoint(A)).decode()

class Keys:
    def __init__(self):
        self.pri_sk = ''
        self.pri_vk = ''
        self.pub_sk = ''
        self.pub_vk = ''
    
    def show(self):
        print()
        print('Private Spend Key:        ',self.pri_sk)
        print('Private View Key:         ',self.pri_vk)
        print('Public Spend Key:         ',self.pub_sk)
        print('Publice View Key:         ',self.pub_vk)
    
    def from_seed(self,s:Seed):
        self.pri_sk = s.hexseed
        self.pub_sk = publickey(self.pri_sk)
        self.pri_vk = sc_reduce32(cn_fast_hash(s.hexseed))
        self.pub_vk = publickey(self.pri_vk)


if __name__ == '__main__':
    print(__file__)
    print('Test Private Spend Key:        ',test_private_spend_key)
    print('Test Private View Key:         ',test_private_view_key)
    print('Test Public Spend Key:         ',test_public_spend_key)
    print('Test Publice View Key:         ',test_public_view_key)
    s = Seed()
    s.from_seed(test_mnemonic_seed)
    k = Keys()
    k.from_seed(s)
    k.show()