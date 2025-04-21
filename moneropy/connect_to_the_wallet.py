from monero.wallet import Wallet
from monero.backends.jsonrpc import JSONRPCWallet

w = Wallet()

print(w.address())
#A2GmyHHJ9jtUhPiwoAbR2tXU9LJu2U6fJjcsv3rxgkVRWU6tEYcn6C1NBc7wqCv5V7NW3zeYuzKf6RGGgZTFTpVC4QxAiAX

print(w.balance())
#Decimal('0E-12')

print(w.seed().hex)

#w = JSONRPCWallet()

#print(w.addresses())
#print(w.address_balance())
