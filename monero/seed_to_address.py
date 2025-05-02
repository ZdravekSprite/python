from config import *
from dependencies.words import WORDS as wordset

import binascii
import operator as _oper

def mn_decode(str):
    out = ''
    n = len(wordset);
    wlist = str.split(' ')
    for i in range(0,24,3):
        w1 = wordset.index(wlist[i])
        w2 = wordset.index(wlist[i+1])
        w3 = wordset.index(wlist[i+2])
        x = w1 + n * (((n - w1) + w2) % n) + n * n * (((n - w2) + w3) % n)
        out += mn_swap_endian_4byte(('0000000'+hex(x)[2:])[-8:])
    return out;

def mn_swap_endian_4byte(str):
    return str[6:8] + str[4:6] + str[2:4] + str[0:2]

def bit(h,i):
    return (ord(chr(h[int(i//8)])) >> (i%8)) & 1

def decodeint(s):
    return sum(2**i * bit(s,i) for i in range(256))

def expmod(b,e,m):
    if e == 0: return 1
    t = expmod(b,e//2,m)**2 % m
    if e & 1: t = (t*b) % m
    return t

q = 57896044618658097711785492504343953926634992332820282019728792003956564819949 # 2**255 - 19

def inv(x):
    return expmod(x,q-2,q)

d = -4513249062541557337682894930092624173785641285191125241628941591882900924598840740 # -121665 * inv(121666)

def edwards(P,Q):
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

'''
l = 7237005577332262213973186563042994240857116359379907606001950938285454250989 # 2 ** 252 + 27742317777372353535851937790883648493
def xrecover(y):
    xx = (y*y-1) * inv(d*y*y+1)
    x = expmod(xx,(q+3)//8,q)
    if (x*x - xx) % q != 0: x = (x*l) % q
    if x % 2 != 0: x = q-x
    return x
By = 4 * inv(5)
Bx = xrecover(By)
'''

B = [15112221349535400772501151409588531511454012693041857206046113283949847762202, 46316835694926478169428394003475163141307993866256225615783033603165251855960] # [Bx % q,By % q]

int2byte = _oper.methodcaller("to_bytes", 1, "big")

def encodepoint(P):
    x,y = P
    bits = [(y >> i) & 1 for i in range(255)] + [x & 1]
    return b''.join([int2byte(sum([bits[i * 8 + j] << j for j in range(8)])) for i in range(32)])

def publickey(sk):
    sk = binascii.unhexlify(sk)
    a = decodeint(sk)
    A = scalarmult(B,a)
    return binascii.hexlify(encodepoint(A)).decode()

#pip install pycryptodome
from Crypto.Hash import keccak
def cn_fast_hash(str):
    k = keccak.new(digest_bits=256)
    k.update(bytearray.fromhex(str))
    return k.hexdigest()

l = 7237005577332262213973186563042994240857116359379907606001950938285454250989 # 2 ** 252 + 27742317777372353535851937790883648493

def reverse_byte_order(hex):
    hex = '0'*(64-len(hex)) + hex
    return "".join(reversed([hex[i*2:i*2+2] for i in range(32)]))

def sc_reduce32(key):
    return reverse_byte_order("%x" % (int(reverse_byte_order(key), 16) % l))

def _hexToBin(hex):
    if len(hex) % 2 != 0:
        return "Hex string has invalid length!"
    return [int(hex[i*2:i*2+2], 16) for i in range(len(hex)//2)]

__encodedBlockSizes = [0, 2, 3, 5, 6, 7, 9, 10, 11]
__alphabet = [ord(c) for c in '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz']

def _uint8be_to_64(data):
    l_data = len(data)

    if l_data < 1 or l_data > 8:
        return "Invalid input length"

    res = 0
    for i in range(l_data):
        res = res << 8 | data[i]
    return res

def split_int(num,base):
    return num // base, num % base

def encode_block(data, buf, index):
    l_data = len(data)

    if l_data < 1 or l_data > 11:
        return "Invalid block length: " + str(l_data)

    num = _uint8be_to_64(data)
    i = __encodedBlockSizes[l_data] - 1

    while num > 0:
        num,remainder = split_int(num,58)
        buf[index+i] = __alphabet[remainder];
        i -= 1

    return buf

def _binToStr(bin):
    return ''.join([chr(bin[i]) for i in range(len(bin))])

def encode(hex):
    data = _hexToBin(hex)
    l_data = len(data)

    if l_data == 0:
        return ""

    full_block_count,last_block_size = split_int(l_data,8)
    res_size = full_block_count * 11 + __encodedBlockSizes[last_block_size]

    res = [0] * res_size
    for i in range(res_size):
        res[i] = __alphabet[0]

    for i in range(full_block_count):
        res = encode_block(data[(i*8):(i*8+8)], res, i * 11)

    if last_block_size > 0:
        res = encode_block(data[(full_block_count*8):(full_block_count*8+last_block_size)], res, full_block_count * 11)

    return _binToStr(res)

def encode_addr(publicSpendKey, publicViewKey):
    data = "12" + publicSpendKey + publicViewKey
    checksum = cn_fast_hash(data)
    return encode(data + checksum[0:8])

def print_all():
    print('Mnemonic Seed:     ',test_mnemonic_seed)
    print()
    hexadecimal_seed = mn_decode(test_mnemonic_seed)
    print('hexadecimal_seed:  ',hexadecimal_seed)
    print('Hexadecimal Seed:  ',test_hexadecimal_seed)
    print()
    private_spend_key = hexadecimal_seed
    print('private_spend_key: ',private_spend_key)
    print('Private Spend Key: ',test_private_spend_key)
    print()
    public_spend_key = publickey(private_spend_key)
    print('Public Spend Key:  ',test_public_spend_key)
    print('public_spend_key:  ',public_spend_key)
    print()
    private_view_key = sc_reduce32(cn_fast_hash(hexadecimal_seed))
    print('Private View Key:  ',test_private_view_key)
    print('private_view_key:  ',private_view_key)
    print()
    public_view_key = publickey(private_view_key)
    print('Public View Key:   ',test_public_view_key)
    print('public_view_key:   ',public_view_key)
    print()
    monero_public_address = encode_addr(public_spend_key,public_view_key)
    print('Public Address:',test_public_address)
    print('encode_addr:   ',monero_public_address)

def seed_to_addr(seed):
    print('Mnemonic Seed: ',seed)
    hexadecimal_seed = mn_decode(seed)
    private_spend_key = hexadecimal_seed
    public_spend_key = publickey(private_spend_key)
    private_view_key = sc_reduce32(cn_fast_hash(hexadecimal_seed))
    public_view_key = publickey(private_view_key)
    public_address = encode_addr(public_spend_key,public_view_key)
    print('Public Address:',public_address)

if __name__ == '__main__':
    print(__file__)
    print_all()
    #seed_to_addr(test_mnemonic_seed)
