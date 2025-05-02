import sys,os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import *

from words25 import words25
from hexseed import mn_decode

#pip install pycryptodome
from Crypto.Hash import keccak
def cn_fast_hash(str):
    k = keccak.new(digest_bits=256)
    k.update(bytearray.fromhex(str))
    return k.hexdigest()

l = 2 ** 252 + 27742317777372353535851937790883648493

def reverse_byte_order(hex):
    if(len(hex)%2==1): hex = '0' + hex
    return "".join(reversed([hex[i:i+2] for i in range(0, len(hex), 2)]))

def sc_reduce32(key):
    reverse = reverse_byte_order("%x" % int((int(reverse_byte_order(key), 16) % l)))
    if len(reverse) == 62:
        reverse += "00"
    return reverse
    #return reverse_byte_order("%x" % int((int(reverse_byte_order(key), 16) % l)))

'''
var privSk = sc_reduce32(hs);
var privVk = sc_reduce32(cn_fast_hash(privSk));

    this.sc_reduce32 = function(hex) {
        var input = hextobin(hex);
        if (input.length !== 32) {
            throw "Invalid input length";
        }
        var mem = Module._malloc(32);
        Module.HEAPU8.set(input, mem);
        Module.ccall('sc_reduce32', 'void', ['number'], [mem]);
        var output = Module.HEAPU8.subarray(mem, mem + 32);
        Module._free(mem);
        return bintohex(output);
    };

    this.cn_fast_hash = function(input, inlen) {
        /*if (inlen === undefined || !inlen) {
            inlen = Math.floor(input.length / 2);
        }*/
        if (input.length % 2 !== 0 || !this.valid_hex(input)) {
            throw "Input invalid";
        }
        //update to use new keccak impl (approx 45x faster)
        //var state = this.keccak(input, inlen, HASH_STATE_BYTES);
        //return state.substr(0, HASH_SIZE * 2);
        return keccak_256(hextobin(input));
    };
    '''

if __name__ == '__main__':
    print(__file__)
    print('Mnemonic Seed:',test_mnemonic_seed)
    print('25 words seed:',words25(" ".join(test_mnemonic_seed.split(" ")[:24])))
    print('Hexadecimal Seed:',test_hexadecimal_seed)
    print('mn_decode:       ',mn_decode(test_mnemonic_seed))
    print('Private View Key:             ',test_private_view_key)
    print('cn_fast_hash:                 ',cn_fast_hash(test_hexadecimal_seed))
    print('sc_reduce32(cn_fast_hash):    ',sc_reduce32(cn_fast_hash(test_hexadecimal_seed)))
