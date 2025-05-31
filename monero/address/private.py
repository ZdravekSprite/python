import sys,os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import *

from monero.seed import Seed
from words25 import words25
from hexseed import mn_decode

from binascii import hexlify, unhexlify

def sc_reduce32(hex):
    input = unhexlify(hex)
    output = hexlify(input)
    return output

import nacl.bindings
#pip install pycryptodome
from Crypto.Hash import keccak

def scalar_reduce(v):
    return nacl.bindings.crypto_core_ed25519_scalar_reduce(v + (64 - len(v)) * b"\0")

def secret_spend_key(hex):
    a = unhexlify(hex)
    return hexlify(scalar_reduce(a)).decode()

def secret_view_key(hex):
    b = scalar_reduce(unhexlify(hex))
    k = keccak.new(digest_bits=256)
    k.update(b)
    return hexlify(scalar_reduce(k.digest())).decode()


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
    seed = Seed(test_mnemonic_seed)
    seed = Seed()
    print('Mnemonic Seed:',seed.phrase)
    print('25 words seed:',words25(" ".join(seed.phrase.split(" ")[:24])))
    print('Hexadecimal Seed:        ',seed.hex)
    print('mn_decode:               ',mn_decode(seed.phrase))
    print()
    print('Private View Key:                      ',seed.secret_view_key())
    print('secret_view_key(hex):                  ',secret_view_key(seed.hex))
    print('Private Spend Key:                     ',seed.secret_spend_key())
    print('secret_spend_key(hex):                 ',secret_spend_key(seed.hex))