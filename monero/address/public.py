import sys,os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import *

from words25 import words25
from hexseed import mn_decode
from private import cn_fast_hash,sc_reduce32

import binascii
import operator as _oper

from monero.seed import Seed

int2byte = _oper.methodcaller("to_bytes", 1, "big")

'''
var pubVk = sec_key_to_pub(privVk);
var pubSk = sec_key_to_pub(privSk);
    this.sec_key_to_pub = function(sec) {
        var input = hextobin(sec);
        if (input.length !== 32) {
            throw "Invalid input length";
        }
        var input_mem = Module._malloc(KEY_SIZE);
        Module.HEAPU8.set(input, input_mem);
        var ge_p3 = Module._malloc(STRUCT_SIZES.GE_P3);
        var out_mem = Module._malloc(KEY_SIZE);
        Module.ccall('ge_scalarmult_base', 'void', ['number', 'number'], [ge_p3, input_mem]);
        Module.ccall('ge_p3_tobytes', 'void', ['number', 'number'], [out_mem, ge_p3]);
        var output = Module.HEAPU8.subarray(out_mem, out_mem + KEY_SIZE);
        Module._free(ge_p3);
        Module._free(input_mem);
        Module._free(out_mem);
        return bintohex(output);
    };
'''

b = 256

def bit(h,i):
    #print(len(h))
    #print(h,len(h),i,int(i//8),i%8)
    return (ord(chr(h[int(i//8)])) >> (i%8)) & 1

def decodeint(s):
    #print(len(s))
    return sum(2**i * bit(s,i) for i in range(0,b))

q = 2**255 - 19

def expmod(b,e,m):
    if e == 0: return 1
    t = expmod(b,e//2,m)**2 % m
    if e & 1: t = (t*b) % m
    return t

def inv(x):
    return expmod(x,q-2,q)

d = -121665 * inv(121666)

def edwards(P,Q,debug=False):
    x1,y1 = P
    x2,y2 = Q
    x3 = (x1*y2+x2*y1) * inv(1+d*x1*x2*y1*y2)
    y3 = (y1*y2+x1*x2) * inv(1-d*x1*x2*y1*y2)
    if debug:
        print('x1:                              ',x1)
        print('x2:                              ',x2)
        print('x3:                              ',x3)
        print('y1:                              ',y1)
        print('y2:                              ',y2)
        print('y3:                              ',y3)
        print('q:                               ',q)
        print('x3q:                             ',x3 % q)
        print('y3q:                             ',y3 % q)
    return [x3 % q,y3 % q]

def scalarmult(P,e,debug=False):
    if e == 0: return [0,1]
    Q = scalarmult(P,e//2,debug)
    Q = edwards(Q,Q)
    if e & 1:
        if debug:
            print('e & 1:                           ',e)
            print('Q:                               ',Q)
        Q = edwards(Q,P,True)
        if debug:
            print('Q:                               ',Q)
    if debug:
        print('scalarmult(P,e)')
        print('B:                               ',B)
        print('P:                               ',P)
        print('e:                               ',e)
        print('Q:                               ',Q)
        print()
    return Q

def encodepoint(P,debug=False):
    x = P[0]
    y = P[1]
    bits = [(y >> i) & 1 for i in range(b-1)] + [x & 1]
    if debug:
        print('encodepoint(P)')
        print('P=(x,y):                         ',P)
        print('bits:                            ',''.join([str(b) for b in bits]),len(bits))
    return b''.join([int2byte(sum([bits[i * 8 + j] << j for j in range(8)])) for i in range(b//8)])

l = 2 ** 252 + 27742317777372353535851937790883648493

def xrecover(y):
    xx = (y*y-1) * inv(d*y*y+1)
    x = expmod(xx,(q+3)//8,q)
    if (x*x - xx) % q != 0: x = (x*l) % q
    if x % 2 != 0: x = q-x
    return x

def getB():
    By = 4 * inv(5)
    Bx = xrecover(By)
    return [Bx % q,By % q]

B = getB()

def publickey(sk,debug=False):
    sk = binascii.unhexlify(sk)
    try:
        a = decodeint(sk)
    except Exception as ex:
        print(ex,sk,len(sk))
    if debug:
        print('publickey(sk)')
        print('sk:                              ',binascii.hexlify(sk))
        print('binascii.unhexlify(sk):          ',sk)
        print('B:                               ',B)
        print('a = decodeint(sk):               ',a)
    A = scalarmult(B,a,debug)
    if debug:
        print('B:                               ',B)
        print('a = decodeint(sk):               ',a)
        print('A = scalarmult(B,a):             ',A)
        print('encodepoint(A):                  ',encodepoint(A,debug))
        print('binascii.hexlify(encodepoint(A)):',binascii.hexlify(encodepoint(A)))
    return binascii.hexlify(encodepoint(A)).decode()

def depublickey(pk,debug=False):
    pk = binascii.unhexlify(pk)
    bits = get_bits([i for i in pk])
    A_get=['neparan' if bits[-1] else 'paran',get_y(bits)]

    if debug:
        print('depublickey(pk)')
        print('pk:                              ',binascii.hexlify(pk))
        print('binascii.unhexlify(pk):          ',pk)
        print('bits:                            ',''.join([str(b) for b in bits]),len(bits))
        print('A*:                              ',A_get)

def get_bits(join_int):
    bits_list=[]
    for int in join_int:
        mini_list = []
        for x in [128,64,32,16,8,4,2,1]:
            mini_list = [int//x]+mini_list
            int = int%x
        bits_list+=mini_list
    return bits_list

def get_y(bits):
    y=0
    multi=1
    for i in bits[:-1]:
        y+=multi*i
        multi*=2
        #print(y,multi)
    return y

'''
def scalarmult(P,e):
    if e == 0: return [0,1]
    Q = scalarmult(P,e//2)
    Q = edwards(Q,Q)
    if e & 1: Q = edwards(Q,P) # P = B
    return Q
def edwards(P,Q):
    x1,y1 = P
    x2,y2 = Q
    x3 = (x1*y2+x2*y1) * inv(1+d*x1*x2*y1*y2)
    y3 = (y1*y2+x1*x2) * inv(1-d*x1*x2*y1*y2)
    return [x3 % q,y3 % q]
'''
def print_all():
    print('Mnemonic Seed:            ',test_mnemonic_seed)
    print('25 words seed:            ',words25(" ".join(test_mnemonic_seed.split(" ")[:24])))
    test_seed = Seed(test_mnemonic_seed)
    print('Hexadecimal Seed:         ',test_seed.hex_seed())
    print('mn_decode:                ',mn_decode(test_mnemonic_seed))
    print('Private Spend Key:        ',test_seed.secret_spend_key())
    print('Private View Key:         ',test_seed.secret_view_key())
    print('cn_fast_hash:             ',cn_fast_hash(test_seed.hex_seed()))
    print('sc_reduce32(cn_fast_hash):',sc_reduce32(cn_fast_hash(test_seed.hex_seed())))
    print('Public Spend Key:         ',test_seed.public_spend_key())
    print('publickey(spend):         ',publickey(test_seed.secret_spend_key()))
    print('Public View Key:          ',test_seed.public_view_key())
    print('publickey(view):          ',publickey(test_seed.secret_view_key()))

def print_reverse_view():
    test_seed = Seed(test_mnemonic_seed)
    print('Private View Key:         ',test_seed.secret_view_key())
    print('publickey(view):          ',publickey(test_seed.secret_view_key(),True))
    print('Public View Key:          ',test_seed.public_view_key())
    print('----------------')
    print('Public View Key:          ',test_seed.public_view_key())
    print('depublickey(view):        ',depublickey(test_seed.public_view_key(),True))
    print('Private View Key:         ',test_seed.secret_view_key())

def print_reverse_spend():
    test_seed = Seed(test_mnemonic_seed)
    print("seed:                         ",test_mnemonic_seed)
    print('mn_decode(seed):              ',mn_decode(test_mnemonic_seed))
    print("hex:                          ",test_seed.hex_seed())
    print("Private Spend Key:            ",test_seed.secret_spend_key())
    print('publickey(spend):             ',publickey(test_seed.secret_spend_key(),True))
    print("Public Spend Key:             ",test_seed.public_spend_key())
    print('----------------')
    print('Public Spend Key:             ',test_seed.public_spend_key())
    print('depublickey(spend):           ',depublickey(test_seed.public_spend_key(),True))
    print('Private Spend Key:            ',test_seed.secret_spend_key())

if __name__ == '__main__':
    print(__file__)
    #print_all()
    print_reverse_spend()
