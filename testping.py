import os
def ping(address):
    return not os.system('ping %s -n 1' % (address,))
for x in range(15):
    if ping("172.20.10."+str(x)):
        print(x)
        exit