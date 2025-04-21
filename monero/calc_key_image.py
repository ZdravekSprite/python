import dependencies.ed25519_changed as ed25519
from dependencies.util import *

#pip install pycryptodome
from Crypto.Hash import keccak
def cn_fast_hash(str):
    k = keccak.new(digest_bits=256)
    k.update(bytearray.fromhex(str))
    return k.hexdigest()

def calc_key_image(a: bytes, b: bytes, R: bytes, i:int) -> bytes:
    """Calculate key image for input 

    Args:
        a: bytes; Private view key
        b: bytes; Private spend key 
        R: bytes; Transaction public key (rG) of refferenced output transaction. Stored in field extra[1:33]).hex(). 
        i: int; output index of refferenced output

    Returns:
        Key image : string
    """
    
    # x = H_s(aR) + b
    aR = ed25519.encodepoint(ed25519.scalarmult(ed25519.decodepoint(R), ed25519.decodeint(a)))
    aR =  ed25519.encodepoint(ed25519.scalarmult(ed25519.decodepoint(aR),  8 )) # There is a mathematical reason for this...
    aR += bytes([i])

    #Hs = sc_reduce32(keccak_256(aR).digest())
    Hs = sc_reduce32(keccak.new(data=aR,digest_bits=256).digest())

    x = int.from_bytes(Hs, byteorder='little') + int.from_bytes(b, byteorder='little')
    x = x % ed25519.l
    x = x.to_bytes(32, 'little')    

    Hp = hashToPointCN(ed25519.publickey(x))
    return ed25519.encodepoint(ed25519.scalarmult(Hp, ed25519.decodeint(x)))

if __name__ == '__main__':
    print(__file__)
    a=b'9c2edec7636da3fbb343931d6c3d6e11bcd8042ff7e11de98a8d364f31976c04' #Private view key
    b=b'950b90079b0f530c11801ef29e99618d3768d79d3d24972ff4b6fd9687b7b20c' #Private spend key
    R=b'8957a240ce4802637d38d8e12d31a3f8d27dc9f5c2713395419b95e422cfe088' #Transaction public key (rG) of refferenced output transaction. Stored in field extra[1:33]).hex(). 
    i=0   #output index of refferenced output
    print(calc_key_image(a, b, R, i))
    '''
Private spend key: <950b90079b0f530c11801ef29e99618d3768d79d3d24972ff4b6fd9687b7b20c>
Public spend key : <287e4f75723d62f0fab06a58893535adc8082f7834c462f30158cecc3e8af327>

Private view key : <9c2edec7636da3fbb343931d6c3d6e11bcd8042ff7e11de98a8d364f31976c04>
Public view key  : <6cc88f08944d5f3b4f811ae011436fbcadc668b566883ce34d06395f450288e4>

Monero address   : <43A7NUmo5HbhJoSKbw9bRWW4u2b8dNfhKheTR5zxoRwQ7bULK5TgUQeAvPS5EVNLAJYZRQYqXCmhdf26zG2Has35SpiF1FP>

Mnemonic seed    : hookup hijack imagine touchy audio bowling gnaw scenic rapid oncoming shrugged gang fazed unhappy lumber amply altitude duties ozone silk hashing feel tolerant uptight tolerant


********************************************************************
Transaction: 1
********************************************************************

tx hash          : <ead7b392f57311fbac14477c4a50bee935f1dbc06bf166d219f4c011ae1dc398>
public tx key    : <8957a240ce4802637d38d8e12d31a3f8d27dc9f5c2713395419b95e422cfe088>
derived key      : <928d282ead4b330ff4aaaa7b505e2cbbb2be219bc9239a7d5ad6a618d83d2841>

Output no: 0, <ae8c1e5c9aff17e29ed6f25fc69120f5356c065140da52c17af97ef6595ba2db>, key_image: <d89cc46e14ac6251b811964735b8fff82dc6b5534339d137d65144e8c78e798a>, mine key: 0.040000000000
Output no: 1, <7b96c0bb8c177b485f99b84d2d446d480e6584de6d3a38c69dd32e0d480e673a>, key_image: <dafab55eead3b665f8db0b86e5c3d87320bbf3e05624539224f0316d76d377b0>, mine key: 0.200000000000
Output no: 2, <b9612c9ce5924816b12ca59a6225d4fc86aaec26041a56b1fb82c1d6897beeb3>, key_image: <1b5baf945a81ac4c48add88af115ca9481ee0647f79d813ae63f8ed2cec54afc>, mine key: 2.000000000000

Total xmr received: 2.240000000000

Input no: 0, <84bd11a888a0666e62f989ad1282c7f1ec107a744d09f0f55f71394e85da400a>, not mine key image
Input no: 1, <682226e7bb46aa71f64c5de90b34d0bf93caa947831e3f64a66c134e0b3b1fe4>, not mine key image
Input no: 2, <b75fb25b08a55572284e4312c658b772617dec74fc603d764d47627fa1cef6f5>, not mine key image
Input no: 3, <ae0b3e22bf5dca03da1b82848f120049b51f1b0f3dbe40e76ca5d5ba796ac1d5>, not mine key image
Input no: 4, <ad3b9a85e6ed25bce75af4dca670ee564a4ba74b58c8289ad10c286df2241a99>, not mine key image

Total xmr spend: 0.000000000000

Summary for tx: <ead7b392f57311fbac14477c4a50bee935f1dbc06bf166d219f4c011ae1dc398>
 - xmr received: 2.240000000000

After this tx, total balance is: 2.240000000000
    '''