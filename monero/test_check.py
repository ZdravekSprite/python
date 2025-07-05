import datetime as dt
import binascii
import varint

#pip install monero
from monero.seed import Seed
from monero import ed25519
from monero.keccak import keccak_256

def make_address_row(hex):
    seed = Seed(hex)
    seed.public_spend_key()
    seed.public_view_key()
    csv_row_dict = {
        'hex':seed.hex,
        'address':str(seed.public_address()),
        'svk':str(seed.secret_view_key()),
        'psk':str(seed.public_spend_key()),
        'block':-1,
        'outputs':0
    }
    return csv_row_dict

def generate_key_derivation(pub, sec, debug=False):
    svk = binascii.unhexlify(sec)
    svk_2 = ed25519.scalar_add(svk, svk)
    svk_4 = ed25519.scalar_add(svk_2, svk_2)
    svk_8 = ed25519.scalar_add(svk_4, svk_4)
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
    print('hsdata',hsdata)
    Hs_ur = keccak_256(hsdata).digest()
    print('Hs_ur',Hs_ur)
    Hs = ed25519.scalar_reduce(Hs_ur)
    print('Hs',Hs)
    HsB = ed25519.scalarmult_B(Hs)
    print('HsB',HsB)
    print('psk',psk)
    k = ed25519.edwards_add(
        HsB,
        psk,
    )
    print('k',k)
    return binascii.hexlify(k).decode()

def check_output(output_row,address_row):
    #output_row block_no,transaction_hash,pub,output_no,output_key
    #address_row address,hex,block,outputs
    #addr = Seed(address_row['hex'])
    pub = output_row['pub']
    sec = address_row['svk']
    print('pub',pub)
    print('sec',sec)
    der = generate_key_derivation(pub, sec)
    print('der',der)
    #spk = base58.decode(address_row['address'])[2:66]
    spk = address_row['psk']
    #print(spk,address_row['psk'])
    print('spk',spk)
    print('output_no',output_row['output_no'])
    pubkey = derive_public_key(der, int(output_row['output_no']), spk)
    print('pubkey',pubkey)
    del address_row['svk']
    del address_row['psk']
    '''
    if address_row['address'] in real_address:
        print('\nreal',address_row)
        #r_fieldnames = ['address','hex']
        r_fieldnames = address_row.keys()
        real_row = address_row
        csv_file_path = path(f'real.csv',['logs'])
        csv_dict_adder(csv_file_path,[real_row],r_fieldnames)

    if pubkey == output_row['output_key']:
        print(output_row,address_row)
        c_fieldnames = ['block_no','transaction_hash','pub','output_no','output_key','address','hex']
        confirm_row = output_row
        confirm_row['address']=address_row['address']
        confirm_row['hex']=address_row['hex']
        csv_file_path = path(f'confirmed.csv',['logs'])
        csv_dict_adder(csv_file_path,[confirm_row],c_fieldnames)
    '''
    k = binascii.unhexlify(pubkey.encode())
    print('k',k)
    return pubkey == output_row['output_key']

if __name__ == '__main__':
    print(__file__)
    '''
    block_no,transaction_hash,pub,output_no,output_key,address,hex
    834112,
    ead7b392f57311fbac14477c4a50bee935f1dbc06bf166d219f4c011ae1dc398,
    8957a240ce4802637d38d8e12d31a3f8d27dc9f5c2713395419b95e422cfe088,
    0,
    ae8c1e5c9aff17e29ed6f25fc69120f5356c065140da52c17af97ef6595ba2db,
    43A7NUmo5HbhJoSKbw9bRWW4u2b8dNfhKheTR5zxoRwQ7bULK5TgUQeAvPS5EVNLAJYZRQYqXCmhdf26zG2Has35SpiF1FP,
    950b90079b0f530c11801ef29e99618d3768d79d3d24972ff4b6fd9687b7b20c
    '''
    hex = '950b90079b0f530c11801ef29e99618d3768d79d3d24972ff4b6fd9687b7b20c'
    print('start:',dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    output_row = {
        'block_no':834112,
        'transaction_hash':'ead7b392f57311fbac14477c4a50bee935f1dbc06bf166d219f4c011ae1dc398',
        'pub':'8957a240ce4802637d38d8e12d31a3f8d27dc9f5c2713395419b95e422cfe088',
        'output_no':0,
        'output_key':'ae8c1e5c9aff17e29ed6f25fc69120f5356c065140da52c17af97ef6595ba2db'
    }
    address_row = make_address_row(hex)
    print(check_output(output_row,address_row))
    print('end:  ',dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),' '*20)