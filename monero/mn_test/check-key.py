import sys,os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import *

#pip install requests
import requests

b = 256

def bit(h,i):
  return (h[i//8] >> (i%8)) & 1

def decodeint(s):
  return sum(2**i * bit(s,i) for i in range(0,b))

def expmod(b,e,m):
  if e == 0: return 1
  t = expmod(b,e//2,m)**2 % m
  if e & 1: t = (t*b) % m
  return t

q = 2**255 - 19

def inv(x):
  return expmod(x,q-2,q)

d = -121665 * inv(121666)

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
  Q = scalarmult(P,e//2)
  Q = edwards(Q,Q)
  if e & 1: Q = edwards(Q,P)
  return Q

I = expmod(2,(q-1)//4,q)

def xrecover(y):
  xx = (y*y-1) * inv(d*y*y+1)
  x = expmod(xx,(q+3)//8,q)
  if (x*x - xx) % q != 0: x = (x*I) % q
  if x % 2 != 0: x = q-x
  return x

By = 4 * inv(5)
Bx = xrecover(By)
B = [Bx % q,By % q]

def encodepoint(P):
  x = P[0]
  y = P[1]
  bits = [(y >> i) & 1 for i in range(b - 1)] + [x & 1]
  return b''.join([bytes([sum([bits[i * 8 + j] << j for j in range(8)])]) for i in range(b//8)])

def publickey(sk):
  a = decodeint(sk)
  A = scalarmult(B,a)
  return encodepoint(A)

import binascii

def str2b(hex_):
    return binascii.unhexlify(hex_)
   
class Key:
    def __init__(self):
        self.private = b""
        self.public = b""
        self.derivation = b""

    def from_hex(self, hex_string):
        self.private = bytes.fromhex(hex_string)
        self.public = publickey(self.private)
    
    def from_seed(self, monero_seed):
       print(monero_seed)

    def show(self):
        print("private spend key: ", self.private.hex())
        print("public spend key:  ", self.public.hex())


if __name__ == '__main__':
    print(__file__)
# Alice generates a random number r ∈R Zl,
# and calculates the one-time public key
#Ko = Hn(rKvB)G + KsB
# Alice sets Ko as the addressee of the payment,
# adds the value rG to the transaction data,
# and submits it to the network.

#Ko = Hn(rKvB)G + KsB = (Hn(rKvB) + ksB)G
#ko = Hn(rKvB) + ksB
    k = Key()
    k.from_hex(hex_string)
    k.show()

    #headers = {"Authorization": f"Token {token}"}
    #link = 'http://localhost:3000/transactions'
    #response = requests.post(link, json=json, headers=headers)
    #json_post = test_json_post

    json_post = {
        "private": kvB,
        "public": KsB,
        "outputNum": 6,
        "extra": [1, 162, 41, 48, 191, 189, 189, 81, 246, 212, 9, 50, 120, 159, 73, 20, 41, 126, 209, 45, 165, 215, 62, 155, 198, 33, 245, 107, 186, 104, 186, 228, 158],
    }

    #reqUrl = 'http://localhost:3000/transactions'
    #response = requests.post(reqUrl, json=json_post)
    #print(response.status_code)
    #print(response.json())

