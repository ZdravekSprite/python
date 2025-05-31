from config import *

from binascii import hexlify, unhexlify, crc32
from os import urandom
import varint
import nacl.bindings

from monero.wordlists.english import English
from monero.seed import Seed
from monero import base58

#pip install pycryptodome
from Crypto.Hash import keccak

word_list = English().word_list

def generate_random_hex(n_bytes=32):
    """Generate a secure and random hexadecimal string. 32 bytes by default, but arguments can override.

    :rtype: str
    """
    h = hexlify(urandom(n_bytes))
    return "".join(h.decode("utf-8"))

def endian_swap(word):
    """Given any string, swap bits and return the result.

    :rtype: str
    """
    return "".join([word[i : i + 2] for i in [6, 4, 2, 0]])

def get_checksum(phrase):
        """Given a mnemonic word string, return a string of the computed checksum.

        :rtype: str
        """
        phrase_split = phrase.split(" ")
        if len(phrase_split) < 24:
            raise ValueError("Invalid mnemonic phrase")
        phrase = phrase_split[:24]
        wstr = "".join(word[:3] for word in phrase)
        wstr = bytearray(wstr.encode("utf-8"))
        z = ((crc32(wstr) & 0xFFFFFFFF) ^ 0xFFFFFFFF) >> 0
        z2 = ((z ^ 0xFFFFFFFF) >> 0) % len(phrase)
        return phrase_split[z2]

def encode(hex):
    """Convert hexadecimal string to mnemonic word representation with checksum."""
    n = 1626
    out = []
    for i in range(len(hex) // 8):
        word = endian_swap(hex[8 * i : 8 * i + 8])
        x = int(word, 16)
        w1 = x % n
        w2 = (x // n + w1) % n
        w3 = (x // n // n + w2) % n
        out += [word_list[w1], word_list[w2], word_list[w3]]
    checksum = get_checksum(" ".join(out))
    out.append(checksum)
    return " ".join(out)

scalar_add = nacl.bindings.crypto_core_ed25519_scalar_add
scalarmult = nacl.bindings.crypto_scalarmult_ed25519_noclamp
edwards_add = nacl.bindings.crypto_core_ed25519_add
scalarmult_B = nacl.bindings.crypto_scalarmult_ed25519_base_noclamp

def scalar_reduce(v):
    return nacl.bindings.crypto_core_ed25519_scalar_reduce(v + (64 - len(v)) * b"\0")

def secret_view_key(hex):
    b = scalar_reduce(unhexlify(hex))
    k256 = keccak.new(digest_bits=256)
    k256.update(b)
    return hexlify(scalar_reduce(k256.digest())).decode()

def generate_key_derivation(pub, sec):
    svk = unhexlify(sec)
    svk_2 = scalar_add(svk, svk)
    svk_4 = scalar_add(svk_2, svk_2)
    svk_8 = scalar_add(svk_4, svk_4)
    shared_secret = scalarmult(svk_8, unhexlify(pub))
    return shared_secret

def derive_public_key(shared_secret, i, spk):
    hsdata = b"".join([
        shared_secret,
        varint.encode(i),
    ])
    k256 = keccak.new(digest_bits=256)
    k256.update(hsdata)
    Hs = scalar_reduce(k256.digest())
    k = edwards_add(
        scalarmult_B(Hs),
        unhexlify(spk),
    )
    return hexlify(k).decode()

def check_output(output_row,address_row):
    #output_row block_no,transaction_hash,pub,output_no,output_key
    #address_row address,hex,block,outputs
    pub = output_row['pub']
    sec = secret_view_key(address_row['hex'])
    der = generate_key_derivation(pub, sec)
    spk = base58.decode(address_row['address'])[2:66]
    pubkey = derive_public_key(der, int(output_row['output_no']), spk)
    return pubkey == output_row['output_key']

if __name__ == '__main__':
    print(__file__)
    seed = Seed()
    #hex = generate_random_hex()
    hex = seed.hex_seed()
    #print(hex)
    #print(encode(hex))
    #print(seed.secret_view_key())
    #print(secret_view_key(hex))
    #print(check_output(first_out_dict,test_address_row))
    #print(check_output(test_output_row,test_address_row))