import datetime as dt
from config import *
from helper_file import *

def int2hexstr(n:int,c=64):
    return format(n, f'0{c}x')

def int2binstr(n:int,c=42):
    return format(n, f'0{c}b')

def bin2hex(bin_):
    return "".join("%02x" % int(b) for b in bin_)

def hex2bin(hex_):
    if len(hex_) % 2 != 0:
        raise ValueError("Hex string has invalid length: %d" % len(hex_))
    return [int(hex_[i : i + 2], 16) for i in range(0, len(hex_), 2)]

def isWin():
    if os.name != 'posix':
        print(os.name)
        #runcmd("dir")
        return True
    else:
        print(os.uname())
        return False

def log_files(start:str):
    return [file for file in files_in_dir(path('',['logs'])) if file[:len(start)].lower() == start.lower()]

def address_files(start='4'):
    return [path(file,['address_csv']) for file in files_in_dir(path('',['address_csv'])) if file[:len(start)].lower() == start.lower()]

def test_if_loged(address:str):
    print(address)
    for f in address_files(address[:2]):
        time_print('now: ',[f])
        csv = csv_dict_reader(f)
        for row in csv:
            #address_row address,hex,block,outputs
            if row['address'] == address: return True

def time_print(prefix,data_list):
    print(prefix,dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), " ".join(data_list), " "*10, end='\r')

if __name__ == '__main__':
    print(__file__)
    print(int2binstr(10))
    print(int2hexstr(100))