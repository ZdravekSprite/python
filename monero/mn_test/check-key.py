from config import *
#pip install requests
import requests
import json

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
    json_post = {
       "status": "OK",
       "transaction_data": {
            "version": 1,
            "unlock_time": 0,
            "vin": [
                { "key": {
                    "amount": 900000000000,
                    "key_offsets": [107079, 58352, 23601, 1168, 56829, 14116, 18588, 7646, 11705, 1135, 4144],
                    "k_image": "191f5fd4e003ab60b28babe46f7ae96a858aed3ed2077324a5edda8308698915"
                } },
                { "key": {
                    "amount": 800000000000,
                    "key_offsets": [126672, 26687, 38902, 26120, 38431, 15204, 23480, 3274, 24393, 21288, 6552],
                    "k_image": "d2624bdf67cb9336df445b6b98485175ebb0e836265b7afb942f4ce19b41c530"
                } }
                ],
            "vout": [
                { "amount": 1000000000, "target": { "key": "cd7064fc8fb5bd308eb205b8600db0ed34302731e7a02f5097bd61878b0df07a" } },
                { "amount": 20000000000, "target": { "key": "bf1e2acf806b89778fc545d610f779903b2b0630dc0fc35dd900a8b6098839cc" } },
                { "amount": 40000000000, "target": { "key": "79a85dc242d70814d0659f1b738d66c515a2d0f9e42d6119b985585cf851ee3e" } },
                { "amount": 300000000000, "target": { "key": "3e77a6dd2b22ff31b5ed9ef472d2bdec9e69f3650c62f6487dffa3b099533f51" } },
                { "amount": 300000000000, "target": { "key": "9a1e997390e116913842363bda1f174b65e87636520b613b62650c831842c263" } },
                { "amount": 1000000000000, "target": { "key": "b4b2a14faf34dc3ecf6b30784aab67af8e8cb62bdae099c5654a29903413776b" } }
            ],
            "extra": [1, 162, 41, 48, 191, 189, 189, 81, 246, 212, 9, 50, 120, 159, 73, 20, 41, 126, 209, 45, 165, 215, 62, 155, 198, 33, 245, 107, 186, 104, 186, 228, 158],
            "signatures": [
                "e24e9c9e6a5125d75153db257aed93557d4804f948bdd00a1a8713fa00a211027b1ba3a9e5324a98d7309b9164df66463c48bf85180e5a3aa9de35eb030c78068feef81f774277f2af98472fad958c3968bd3159329c3c290a97cbb4b1f36d0f3f704bfe2f9af32babbce340227171ae39804e1d19b6914caee7935f0ab45d00477c82a40f65fb1f731d001426d759846c98bce53f61f0301b6a58d0a82289021f3ee7f9d45100ce5cff7fc1b9b0c9da0510267f43410bb4edfe5972724a7804eb5cd00b37fdb66dadc031d7e86759a21fdb4a7beb16ac909b6afeb75142aa06636498729c13f9993c63b460a3bdc5c22a0939b8f8f04c2ded91643f3f67890af74a70df4a53153d67d3d88c85c21572f5310a04d3f365997e17efd8fd09a70ced891d461ce1112ce46b7d19f3e3862529477635ae9ac6ce9a160af2cebf270d087fd2c8fece03578eac1fef2bc33ef6cc08bb1f6c27c893c18965416e47600e22c53647e205011801e04ca5fbd5664eac1338d6aef0b4e957d20847ba88ea09e78858937b4abc6b78d8c8baaf00faef5814eba7a42453980f5a850fdb83d00d3dcfbc460f90dc5243a9ba381cec7e73a5cd99874aa0870d0fd04b0b1bdac609c20dfbb3ac19fd0efe08889d0897a816199e1a950963892337462f91f22b4a06117296e7fe30433e731be094e2446479d52c8fb1278261a5d77191a0f0c86d0d0ef4af40435885aa680b064075297fed7044cc27c5283e0082c09501e502bf01c9a59d3d0af9afa2b2b82e892cb7a505bc4f234e9de08c5d5f9b901693686b0f14170ab9a20650456247e835bd3b98b8f57ea226edd83f34b0f6f635fd3c3d00c592bc25617fe0cf02732b0fdea5c579bd306847074d3981fd6f59e2040ac30a08801043aa3a9a14bd50273184d9995b05c9e45cf9b60ee4483fcadd486e1f0793b27d79f6e95523153366ae300f742b8db582ac728482845837a8dfdd2c090c",
                "0358efda03a199491630933f607848349a87e7b6460f2204e4be61caa76f2b099160961fdd4d9802ed405ab412b7ae07b1dbca05df369718d9f81cc897965609074867c05593d2daffbf3d83828ca4223b8ac9d2f6dc39f376561491ed08c6020cc778ad04f926aa06e2f1ccf7213566efa8d500ec1ecfcbf2f25ae7328c950360b0683aff1a46899f9fa730230f7e32ee6becdec64bc08a7ea8d91f9e5e270ed34b34521f256c2004390ceb02c554b0290917737c9f6f52eb5e7e2f8dfb3d0ad870d27f859bfd0c15730aaa451a3ae2c258ef44a0aaefc63a3e5475e9bc890a67615775401a9399e56eb3a6fac310b226cbdd74b90d20e2c7dc1d5fef37f60cf32bb1e0ef7f6e341a3902c28386ac95d940341d08f0c2d47cfc7119fc9b4a082858171b1fd13a4d92835b852434a0fa0ad758e97f091a832b50b0059535720438a9b74aefa54f62fedf1be5a8a7845d41784184e2ed2f40823b95e1bf57ab036c749e63b7e5d3b207205e09402d3633eca74b3d04237a944974c1f7980e340057502cd561121c54017b20aafe1b251c87439fa8ea184caffdceb6630d0c870543ff0effff37c3b55225443eac7b9337472ca70ef2c53e0009d73590bea5820a9ecd12264aefc2bd2bb2aac3eca25ffd6236d197ff4dd3c9e4e623120443860b44e132dcafb5d472a055548f4713b8dd26cf9270300d7d344c607767ccc28f0f5357353229340cea62ac7b71b6df36aa532ad71936304ead2195451e742cc70783112db8338d190cb3d35086a14c90ea4a44751866a0a0b561aebc48e0a2b009e65f204259e22e50b35cc4f4b340a5b4ff9a153e11903db4121dc960061df60b7e877143ee3d07cb1bb8a8ca8c0e66868461f7b1764806ffae451d947f6484097c4b7a02b3af74fd1162efb40db179c78b9737c01e79b02042c6f936409d8801129bdf8dfb50a48c713ed889923d08cdc5da4f364d46afbcd7485f01c409650e"
            ]
        }
    }

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

