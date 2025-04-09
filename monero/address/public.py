from config import *
from words25 import words25
from hexseed import mn_decode
from private import cn_fast_hash,sc_reduce32
import binascii
import operator as _oper

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

def edwards(P,Q):
    x1 = P[0]
    y1 = P[1]
    x2 = Q[0]
    y2 = Q[1]
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
    x = P[0]
    y = P[1]
    bits = [(y >> i) & 1 for i in range(b-1)] + [x & 1]
    return b''.join([int2byte(sum([bits[i * 8 + j] << j for j in range(8)])) for i in range(b//8)])

l = 2 ** 252 + 27742317777372353535851937790883648493

def xrecover(y):
    xx = (y*y-1) * inv(d*y*y+1)
    x = expmod(xx,(q+3)//8,q)
    if (x*x - xx) % q != 0: x = (x*l) % q
    if x % 2 != 0: x = q-x
    return x

By = 4 * inv(5)
Bx = xrecover(By)
B = [Bx % q,By % q]

def publickey(sk):
    sk = binascii.unhexlify(sk)
    try:
        a = decodeint(sk)
    except Exception as ex:
        print(ex,sk,len(sk))
    A = scalarmult(B,a)
    return binascii.hexlify(encodepoint(A)).decode()

if __name__ == '__main__':
    print(__file__)
    print('Mnemonic Seed:            ',test_mnemonic_seed)
    print('25 words seed:            ',words25(" ".join(test_mnemonic_seed.split(" ")[:24])))
    print('Hexadecimal Seed:         ',test_hexadecimal_seed)
    print('mn_decode:                ',mn_decode(test_mnemonic_seed))
    print('Private Spend Key:        ',test_private_spend_key)
    print('Private View Key:         ',test_private_view_key)
    print('cn_fast_hash:             ',cn_fast_hash(test_hexadecimal_seed))
    print('sc_reduce32(cn_fast_hash):',sc_reduce32(cn_fast_hash(test_hexadecimal_seed)))
    print('Public Spend Key:         ',test_public_spend_key)
    print('publickey(spend):         ',publickey(test_private_spend_key))
    print('Public View Key:          ',test_public_view_key)
    print('publickey(view):          ',publickey(test_private_view_key))
