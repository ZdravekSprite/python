from binascii import hexlify, unhexlify, crc32
from os import urandom

from monero.wordlists.english import English
word_list = English().word_list

import nacl.bindings
scalar_add = nacl.bindings.crypto_core_ed25519_scalar_add
scalarmult = nacl.bindings.crypto_scalarmult_ed25519_noclamp
edwards_add = nacl.bindings.crypto_core_ed25519_add
scalarmult_B = nacl.bindings.crypto_scalarmult_ed25519_base_noclamp

#pip install pycryptodome
from Crypto.Hash import keccak

def scalar_reduce(v):
    return nacl.bindings.crypto_core_ed25519_scalar_reduce(v + (64 - len(v)) * b"\0")

def scalar_reduce_keccak_256(data):
    k256 = keccak.new(digest_bits=256)
    k256.update(data)
    return scalar_reduce(k256.digest())

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

def encode(hex_):
    """Convert hexadecimal string to mnemonic word representation with checksum."""
    n = 1626
    out = []
    for i in range(len(hex_) // 8):
        word = endian_swap(hex_[8 * i : 8 * i + 8])
        x = int(word, 16)
        w1 = x % n
        w2 = (x // n + w1) % n
        w3 = (x // n // n + w2) % n
        out += [word_list[w1], word_list[w2], word_list[w3]]
    checksum = get_checksum(" ".join(out))
    out.append(checksum)
    return " ".join(out)

def variant_encode(number):
    """Pack `number` into varint bytes"""
    buf = b''
    while True:
        towrite = number & 0x7f
        number >>= 7
        if number:
            buf += bytes((towrite | 0x80, ))
        else:
            buf += bytes((towrite,))
            break
    return buf