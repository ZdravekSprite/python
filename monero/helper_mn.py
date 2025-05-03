#pip install monero
from monero.daemon import Daemon
from monero.seed import Seed
from monero import ed25519
from monero import base58
from monero.keccak import keccak_256
import binascii
import varint

def print_seed(seed:Seed):
    print(seed.phrase)
    print(seed.hex)
    print(seed.secret_spend_key())
    print(seed.secret_view_key())
    print(seed.public_spend_key())
    print(seed.public_view_key())
    print(seed.public_address())

def rnd_seed(debug=False):
    #print(Seed().__dict__.keys()) # dict_keys(['phrase', 'hex', 'word_list', '_ed_pub_spend_key', '_ed_pub_view_key'])
    seed = Seed()
    seed.public_spend_key()
    seed.public_view_key()
    if debug: print_seed(seed)
    return seed

def parseExtra(bin):
    extra = {
        'pub': False,
        'paymentId': False
    }
    if bin[0] == 1: #pubkey is tag 1
        extra['pub'] = base58._binToHex(bin[1: 33]) #pubkey is 32 bytes
        #print(bin,len(bin))
        if len(bin)>35 and (bin[33] == 2 and bin[35] == 0 or bin[35] == 1):
            extra['paymentId'] = base58._binToHex(bin[36:36 + bin[34] - 1])
    elif bin[0] == 2:
        if bin[2] == 0 or bin[2] == 1:
            extra['paymentId'] = base58._binToHex(bin[3: 3 + bin[1] - 1])
        #second byte of nonce is nonce payload length; payload length + nonce tag byte + payload length byte should be the location of the pubkey tag
        if bin[2 + bin[1]] == 1:
            offset = 2 + bin[1]
            extra['pub'] = base58._binToHex(bin[offset + 1: offset + 1 + 32])
    return extra

def generate_key_derivation(pub, sec, debug=False):
    svk = binascii.unhexlify(sec)
    if debug:
        print('private_view_key:')
        print('svk:               ',sec,svk)
    svk_2 = ed25519.scalar_add(svk, svk)
    if debug: print('svk2:              ',binascii.hexlify(svk_2).decode(),svk_2)
    svk_4 = ed25519.scalar_add(svk_2, svk_2)
    if debug: print('svk4:              ',binascii.hexlify(svk_4).decode(),svk_4)
    svk_8 = ed25519.scalar_add(svk_4, svk_4)
    if debug:
        print('svk8:              ',binascii.hexlify(svk_8).decode(),svk_8)
        print('pub:               ',pub,binascii.unhexlify(pub))
    shared_secret = ed25519.scalarmult(svk_8, binascii.unhexlify(pub))
    return shared_secret

def derive_public_key(der, i, spk,debug=False):
    shared_secret = der
    psk = binascii.unhexlify(spk)

    hsdata = b"".join(
        [
            shared_secret,
            varint.encode(i),
        ]
    )
    if debug: print('hsdata',binascii.hexlify(hsdata).decode())
    Hs_ur = keccak_256(hsdata).digest()
    if debug: print('Hs_ur',binascii.hexlify(Hs_ur).decode())
    Hs = ed25519.scalar_reduce(Hs_ur)
    if debug: print('Hs',binascii.hexlify(Hs).decode())
    k = ed25519.edwards_add(
        ed25519.scalarmult_B(Hs),
        psk,
    )
    if debug: print('k',binascii.hexlify(k).decode())
    return binascii.hexlify(k).decode()
