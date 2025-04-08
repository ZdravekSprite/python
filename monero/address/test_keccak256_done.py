#pip install pysha3
#import sha3
from hashlib import sha3_256 as sha3
#import ed25519
import binascii
import base58 as _b58
 
b = 256
q = 2**255 - 19
l = 2 ** 252 + 27742317777372353535851937790883648493
 
def expmod(b,e,m):
  if e == 0: return 1
  t = expmod(b,e/2,m)**2 % m
  if e & 1: t = (t*b) % m
  return t
 
def inv(x):
  return expmod(x,q-2,q)
 
d = -121665 * inv(121666)
 
def xrecover(y):
  xx = (y*y-1) * inv(d*y*y+1)
  x = expmod(xx,(q+3)/8,q)
  if (x*x - xx) % q != 0: x = (x*l) % q
  if x % 2 != 0: x = q-x
  return x
 
By = 4 * inv(5)
Bx = xrecover(By)
B = [Bx % q,By % q]
 
 
def reverse_byte_order(hex):
    if(len(hex)%2==1): hex = '0' + hex
    return "".join(reversed([hex[i:i+2] for i in range(0, len(hex), 2)]))
 
def sc_reduce32(key):
    return reverse_byte_order("%x" % int((int(reverse_byte_order(key), 16) % l)))
 
def cn_fast_hash(hex):
    k = sha3.keccak_256()
    k.update(bytearray.fromhex(hex))
    return k.hexdigest()
 
def bit(h,i):
  return (ord(h[i/8]) >> (i%8)) & 1
 
def decodeint(s):
  return sum(2**i * bit(s,i) for i in range(0,b))   
 
def edwards(P,Q):
  x1 = P[0]
  y1 = P[1]
  x2 = Q[0]
  y2 = Q[1]
  x3 = (x1*y2+x2*y1) * inv(1+d*x1*x2*y1*y2)
  y3 = (y1*y2+x1*x2) * inv(1-d*x1*x2*y1*y2)
  return [x3 % q,y3 % q]
 
def scalarmult(P,e):
  if e == 0: return [0,1]
  Q = scalarmult(P,e/2)
  Q = edwards(Q,Q)
  if e & 1: Q = edwards(Q,P)
  return Q
  
def encodepoint(P):
  x = P[0]
  y = P[1]
  bits = [(y >> i) & 1 for i in range(b - 1)] + [x & 1]
  return ''.join([chr(sum([bits[i * 8 + j] << j for j in range(8)])) for i in range(b/8)])
 
def publickey(sk):
  sk = binascii.unhexlify(sk)
  a = decodeint(sk)
  A = scalarmult(B,a)
  return binascii.hexlify(encodepoint(A))
 
def encode_addr(version, publicSpendKey, publicViewKey):
    '''Given address version and public spend and view keys, derive address.'''
    data = version + publicSpendKey + publicViewKey
    checksum = cn_fast_hash(data)
    return _b58.encode(data + checksum[0:8])
 
hexadecimal_seed = "852249bca4446e65501cc7f8338027ec"
hash_of_seed = cn_fast_hash(hexadecimal_seed)
private_spend_key = sc_reduce32(hash_of_seed)
public_spend_key = publickey(private_spend_key)
private_view_key = sc_reduce32(cn_fast_hash(hash_of_seed))
public_view_key = publickey(private_view_key)
monero_public_address = encode_addr("12",public_spend_key,public_view_key)
 
print ("Non-standard Seed = ", hexadecimal_seed)
print ("Normalized Seed   = ", hash_of_seed)
print ("Private Spend Key = ", private_spend_key)
print ("Public Spend Key = ", public_spend_key)
print ("Private View Key  = ", private_view_key)
print ("Public View Key  = ", public_view_key)
print ("Public Address = ", monero_public_address)