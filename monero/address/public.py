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

def getB():
    By = 4 * inv(5)
    Bx = xrecover(By)
    return [Bx % q,By % q]

B = getB()

def publickey(sk):
    sk = binascii.unhexlify(sk)
    try:
        a = decodeint(sk)
    except Exception as ex:
        print(ex,sk,len(sk))
    A = scalarmult(B,a)
    return binascii.hexlify(encodepoint(A)).decode()

def print_all():
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

def print_int2byte(i,bits):
    sum_bits = []
    for j in range(8):
        #print(i,j,bits[i * 8 + j] << j,bits[i * 8 + j],i * 8 + j)
        sum_bits.append(bits[i * 8 + j] << j)
    #print(sum(sum_bits),sum_bits)
    #sum_bits = sum([bits[i * 8 + j] << j for j in range(8)])
    return int2byte(sum(sum_bits))

def print_join(bits):
    #join = [int2byte(sum([bits[i * 8 + j] << j for j in range(8)])) for i in range(32)]
    join=[]
    for i in range(32):
        #join.append(int2byte(sum([bits[i * 8 + j] << j for j in range(8)])))
        join.append(print_int2byte(i,bits))
    print('[sum([bits[i * 8 + j] << j for j in range(8)]) for i in range(b//8)]          ',[sum([bits[i * 8 + j] << j for j in range(8)]) for i in range(b//8)])
    print('[int2byte(sum([bits[i * 8 + j] << j for j in range(8)])) for i in range(b//8)]',join)
    return join

def get_bits(join_int):
    bits_list=[]
    for int in join_int:
        mini_list = []
        for x in [128,64,32,16,8,4,2,1]:
            mini_list = [int//x]+mini_list
            int = int%x
        bits_list+=mini_list
    return bits_list

def print_bits(x,y):
    bits = [(y >> i) & 1 for i in range(255)] + [x & 1]
    #for i in range(255):
    #    print((y >> i) & 1,y,y >> i,i)
    #print([x & 1],x)
    print('[(y >> i) & 1 for i in range(b-1)] + [x & 1]',bits)
    return bits

def get_y(bits):
    y=0
    multi=1
    for i in bits[:-1]:
        y+=multi*i
        multi*=2
        #print(y,multi)
    return y

def print_de98(A):
    print('A:',A)
    #print(encodepoint(A))
    #print('encodepoint(A)')
    x = A[0]
    #print('x = A[0]',f'x = {x}')
    y = A[1]
    #print('y = A[1]',f'y = {y}')
    #print('[x & 1]:',[x & 1])
    bits = print_bits(x,y)
    #join = print_join(bits)
    #encodepoint = b''.join(join)
    #print("b''.join([int2byte(sum([bits[i * 8 + j] << j for j in range(8)])) for i in range(b//8)])",encodepoint)
    #print(binascii.hexlify(encodepoint))
    #print(binascii.hexlify(encodepoint).decode())
    #print('publickey(view):          ',publickey(test_private_view_key))
    #print(test_public_view_key)
    #print(test_public_view_key.encode())
    #print('encodepoint                                                                             ',binascii.unhexlify(test_public_view_key.encode()))
    #all_bytes = bytes(range(256))
    #print('join                                                                          ',[all_bytes[i:i+1] for i in binascii.unhexlify(test_public_view_key.encode())])
    #print('join_int                                                                      ',[i for i in binascii.unhexlify(test_public_view_key.encode())])
    bits_get = get_bits([i for i in binascii.unhexlify(test_public_view_key.encode())])
    print('bits                                        ',bits_get)
    #print('        x = ','neparan' if bits_get[-1] else 'paran')
    #print('        y = ',get_y(bits_get))
    A_get=['neparan' if bits[-1] else 'paran',get_y(bits_get)]
    print('A:',A_get)
    return A_get

def print_edwards(P,Q,n=0):
    x1 = P[0]
    y1 = P[1]
    x2 = Q[0]
    y2 = Q[1]
    x3 = (x1*y2+x2*y1) * inv(1+d*x1*x2*y1*y2)
    y3 = (y1*y2+x1*x2) * inv(1-d*x1*x2*y1*y2)
    if not n: print(x1,y1)
    if not n: print(x2,y2)
    if not n: print('x3:',x3,'\nx3//q:',x3//q)
    if not n: print('y3:',y3,'\ny3//q:',y3//q)
    if not n: print('[x3 % q,y3 % q]',[x3 % q,y3 % q])
    return [x3 % q,y3 % q]

def print_scalarmult(P,e,n=0):
    if not n: print('print_scalarmult(P,e)')
    n+=1
    if e == 0:
        #print('if e == 0: return [0,1]')
        return [0,1]
    #print('Q = scalarmult(P,e//2)')
    Q = print_scalarmult(P,e//2,n)
    #print('Q = edwards(Q,Q)\n\tQ:',Q)
    n-=1
    if not n: print('Q = edwards(Q,Q)\n\tQ old:',Q)
    Q = print_edwards(Q,Q,n)
    if not n: print('\tQ new:',Q)
    if e & 1:
        if not n: print('if e & 1: Q = edwards(Q,P)\n\te:',e,'\n\tQ:',Q,'\n\tP:',P)
        Q = print_edwards(Q,P,n)
        if not n: print('\tQ:',Q)
    return Q

def print_de97(B,a):
    print('a:',a)
    print('B:',B)
    A = print_scalarmult(B,a)
    get_A = print_de98(A)
    print(get_A)
#    if e == 0: return [0,1]
    if get_A == ['paran',1]:
        a = 0
        print('a:',a)

if __name__ == '__main__':
    print(__file__)
    #print_all()
    print('Public View Key:          ',test_public_view_key)
    sk = binascii.unhexlify(test_private_view_key)
    print('sk:',sk)
    a = decodeint(sk)
    print_de97(B,a)

