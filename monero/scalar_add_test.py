import binascii
import nacl.bindings

from config import test_private_view_key
from helper import int2hexstr, int2binstr
from monero.seed import Seed

edwards_add = nacl.bindings.crypto_core_ed25519_add
inv = nacl.bindings.crypto_core_ed25519_scalar_invert
scalar_add = nacl.bindings.crypto_core_ed25519_scalar_add
scalarmult_B = nacl.bindings.crypto_scalarmult_ed25519_base_noclamp
scalarmult = nacl.bindings.crypto_scalarmult_ed25519_noclamp

def add_loop(sec,ren=8):
    sec_int = int(sec,16)
    print(sec, sec_int)
    svk = binascii.unhexlify(sec)
    svk_x = svk

    for x in range(ren):
        svk_x = scalar_add(svk_x, svk)
        sec_x = binascii.hexlify(svk_x).decode()
        sec_x_int = int(sec_x,16)
        print(sec_x, sec_x_int)

def nool_add(sec):
    sec0 = '0'*len(sec)
    unsec0 = binascii.unhexlify(sec0)

    unsec = binascii.unhexlify(sec)
    sec_int = int(sec,16)
    print(sec, sec_int)
    svk = scalar_add(unsec0, unsec)
    hexsvk = binascii.hexlify(svk).decode()
    svk_int = int(hexsvk,16)
    print(hexsvk, svk_int)

def loop_test(sec,loop=5):
    sec0 = '0'*len(sec)
    unsec0 = binascii.unhexlify(sec0)

    unsec = binascii.unhexlify(sec)
    sec_int = int(sec,16)
    print(sec, sec_int)
    print()

    for x in range(loop*2+1):
        secx_int = sec_int - loop + x
        secx_hex = int2hexstr(secx_int)
        unsecx = binascii.unhexlify(secx_hex)

        svk = scalar_add(unsec0, unsecx)
        svk_hex = binascii.hexlify(svk).decode()
        svk_int = int(svk_hex,16)
        #print(secx_hex, secx_int)
        if secx_hex != svk_hex:
            #print(svk_hex, svk_int)
            pass
        else:
            print(secx_hex, secx_int)
            svk_2 = scalar_add(svk, svk)
            svk_4 = scalar_add(svk_2, svk_2)
            svk_8 = scalar_add(svk_4, svk_4)
            print(binascii.hexlify(svk_2).decode(),binascii.hexlify(svk_4).decode(),binascii.hexlify(svk_8).decode())

def test_add_hex(hex1,hex2):
    unhex1 = binascii.unhexlify(hex1)
    unhex2 = binascii.unhexlify(hex2)
    return scalar_add(unhex1, unhex2)

def test_add_int(int1,int2):
    hex1 = int2hexstr(int1)
    hex2 = int2hexstr(int2)
    return test_add_hex(hex1,hex2)

if __name__ == '__main__':
    print(__file__)

    seed = Seed()
    seed.public_spend_key()
    seed.public_view_key()
    sec = seed.secret_view_key()

    #sec = test_private_view_key
    sec = '0'*(len(sec)-2)+'ff'

    #add_loop(sec,32)
    #nool_add(sec)
    loop_test(sec,100)
    #max = 2
    #for x in range(max):
    #    y=100
    #    print(binascii.hexlify(test_add(y+x,y+max-x)).decode(),y+x,y+max-x)
    '''
    sec = '0'*(len(sec)-4)+'0001'
    sec_int = int(sec,16)
    print(1,sec,sec_int)
    sec_2=binascii.hexlify(test_add_hex(sec,sec)).decode()
    sec2_int = int(sec_2,16)
    print(2,sec_2,sec2_int)
    sec_4=binascii.hexlify(test_add_hex(sec_2,sec_2)).decode()
    sec4_int = int(sec_4,16)
    print(4,sec_4,sec4_int)
    '''
    '''
    sec2_int_plus = 2 * sec_int
    sec2_plus = int2hexstr(sec2_int_plus)
    print('+',sec2_plus,'sec2_plus')
    sec4_plus_un=test_add_hex(sec2_plus,sec2_plus)
    sec4_plus=binascii.hexlify(test_add_hex(sec2_plus,sec2_plus)).decode()
    sec4_int_plus = int(sec4_plus,16)
    print('4+',sec4_plus,sec4_int_plus)
    '''
