from config import *
from helper_hex import *

from monero import base58

def secret_spend_key(hex_):
    a = unhexlify(hex_)
    return hexlify(scalar_reduce(a)).decode()

def secret_view_key(hex_):
    b = scalar_reduce(unhexlify(hex_))
    return hexlify(scalar_reduce_keccak_256(b)).decode()

def public_spend_key(hex_):
    return hexlify(scalarmult_B(unhexlify(secret_spend_key(hex_)))).decode()

def public_view_key(hex_):
    return hexlify(scalarmult_B(unhexlify(secret_view_key(hex_)))).decode()

def public_address(hex_):
    netbyte = (18, 53, 24)[0]
    data = "{:x}{:s}{:s}".format(
        netbyte, public_spend_key(hex_), public_view_key(hex_)
    )
    k256 = keccak.new(digest_bits=256)
    k256.update(unhexlify(data))
    checksum = k256.hexdigest()
    return str(base58.encode(data + checksum[0:8]))

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
        variant_encode(i),
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
    
    hex = generate_random_hex()
    from monero.seed import Seed
    seed = Seed(hex)
    
    #hex = seed.hex_seed()
    #print(hex)
    #print(encode(hex))

    print(seed.secret_spend_key())
    print(secret_spend_key(hex))

    print(seed.secret_view_key())
    print(secret_view_key(hex))

    print(seed.public_spend_key())
    print(public_spend_key(hex))

    print(seed.public_view_key())
    print(public_view_key(hex))

    print(seed.public_address())
    print(public_address(hex))
    #print(check_output(first_out_dict,test_address_row))
    #print(check_output(test_output_row,test_address_row))
