import binascii
import nacl.bindings

from config import test_private_view_key

def add_loop(sec):
    sec_int = int(sec,16)
    print(sec, sec_int)
    svk = binascii.unhexlify(sec)
    svk_x = svk

    for x in range(8):
        svk_x = scalar_add(svk_x, svk)
        sec_x = binascii.hexlify(svk_x).decode()
        sec_x_int = int(sec_x,16)
        print(sec_x, sec_x_int)

if __name__ == '__main__':
    print(__file__)

    scalar_add = nacl.bindings.crypto_core_ed25519_scalar_add

    sec = test_private_view_key
    sec = '0'*(len(sec)-2)+'10'
    add_loop(sec)
