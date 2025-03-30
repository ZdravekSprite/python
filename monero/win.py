#monerod.exe
#C:\ProgramData\bitmonero

import subprocess
from subprocess import PIPE, STDOUT
from config import test_argument
from os_help import file_del, path, isWin
from words import *

def getArgument(list):
    return "--electrum-seed="+" ".join(list)

def loopWallet(list):
    for word in list:
        try:
            #print(list+[word])
            #test_wallet(list+[word])
            create_wallet(list+[word])
        except Exception as ex:
            print(ex)

def create_wallet(electrum):
    file_del(path("test"))
    file_del(path("test.keys"))
    file_del(path("monero-wallet-cli.log"))
    program = path("monero-wallet-cli.exe")
    argument1 = "--restore-deterministic-wallet"
    argument3 = "--generate-new-wallet=monero/test"
    argument4 = "--restore-height=3378000"
    commandList = [program, argument1, getArgument(electrum), argument3, argument4] # commandLine

    test00(commandList)

class Test:
    def __init__(self, commandList):
        self.proc = subprocess.Popen(commandList, stdin=PIPE, stdout=PIPE, encoding="utf-8")

    def talk(self, tx):
        self.proc.stdout.flush()
        self.proc.stdout.read()
        print(('TX: ' + tx).rstrip('\r\n'))
        self.proc.stdin.write(tx + '\n')
        rx = self.proc.stdout.readline().rstrip('\r\n')
        print('RX: ' + rx)

    def read(self):
        rx = self.proc.stdout.readline().rstrip('\r\n')
        print('RX: ' + rx)

    def reads(self):
        rx = self.proc.stdout.readlines()
        print('RX: ' + rx)

def test00(commandList):
    try:
        test = Test(commandList)
        print("prije")
        for i in range(6):
            test.read()
        test.talk("\n")
        print("poslije")
    except Exception as ex:
        print('ex',ex)
    if not test.proc.poll():
        test.proc.kill()

def run(self):
    while True:
        line = self.stream.readline()
        if len(line) == 0:
            break
        print(line)

def test01(commandList):
    try:
        proc = subprocess.Popen(commandList, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, encoding="utf-8")
        '''
        while True:
            line = proc.stdout.readline()
            if len(line) == 0:
                break
            print('\t', line.strip())
            if line.strip() == 'Logging to c:\\dev\\python\\monero\\monero-wallet-cli.log':
                print(proc.communicate())
        '''
        proc.stdout.readlines()
        '''
        for line in proc.stdout.readlines():
            print('\t', line.strip())
            if line.strip() == 'Logging to c:\\dev\\python\\monero\\monero-wallet-cli.log':
                print(proc.communicate())
        '''
        #proc.stdin.write("\n")
        #proc.terminate()
        #proc.kill()
        #file_del(path("monero-wallet-cli.log"))
    except Exception as ex:
        print(ex)
    
def test02(commandList):
    result = subprocess.run(commandList, shell=True, capture_output=True, text=True)
    print(result.stdout)

def test03(commandList):
    print('commandList',commandList)
    while True:
        ps = subprocess.Popen(commandList, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT)
        next_line = ps.stdout.readline()
        if not next_line:
            break
        print(next_line)
        ps.stdout.flush()
        #ps.stdout.write(next_line)
        #ps.stdout.flush()
    # input into stdin
    input0 = b"\n"
    input1 = b"test\n"
    input2 = b"N\n"
    input3 = b"exit\n"
    #ps.stdin.write(input0)
    #output = ps.stdout.readline()
    #print(input0,output)
    #ps.stdin.write(input1)
    #ps.stdin.write(input1)
    #ps.stdin.write(input2)
    #ps.stdin.write(input3)
    #print(ps.communicate())

def test04(commandList):
    input0 = b"\n"
    command = subprocess.Popen(commandList, shell=True, stdout=PIPE)
    end_of_pipe = command.stdout
    for line in end_of_pipe:
        print('\t', line.strip())
        #if line.strip() == b'Enter seed offset passphrase, empty if none:':
        #    command.stdin.write(input0)

def test05(commandList):
    proc = subprocess.Popen(commandList, shell=True, stdin=PIPE, stdout=PIPE, encoding="utf-8")
    #output = proc.communicate()[0]
    #print(output)
    #'''
    while True: # Infinite loop
        if proc.poll() is not None:
            break
        output = proc.stdout.readline()
        if output:
            print('\t',output.strip())
        #if output.strip() == b'Logging to c:\\dev\\python\\monero\\monero-wallet-cli.log':
        #    proc.stdin.write(b"\n")
    #'''

def test_wallet(electrum):
    program = path("monero-wallet-cli.exe")
    argument1 = "--restore-deterministic-wallet"
    argument3 = "--generate-new-wallet=monero/test"
    commandList = [program, argument1, getArgument(electrum), argument3] # commandLine
    ps = subprocess.Popen(commandList, shell=False, stdin=PIPE, stdout=PIPE, stderr=STDOUT)
    output = ps.communicate()[0].split(b'\n')
    if output[-2]!=b'Error: Electrum-style word list failed verification\r':
        print("OK?:",electrum)

def callcmd(commandList):
    subprocess.call(commandList, shell=True) #Run under Windows

def runcmd(cmd):
    result = subprocess.run([cmd], shell=True, capture_output=True, text=True)
    print(result.stdout)

if __name__ == '__main__':
    print(__file__)
    if isWin:
        #runcmd("dir")
        #create_wallet()
        #test_words = getRndWords(WORDS)
        #for i in test_words:
        #    random.shuffle(test_words)
        #    loopWallet(test_words)
        create_wallet(['knee', 'noodles', 'serving', 'splendid', 'height', 'ruined', 'bias', 'obliged', 'seventh', 'hobby', 'inmate', 'village', 'taxi', 'match', 'ultimate', 'plywood', 'axis', 'viking', 'atom', 'folding', 'toffee', 'waveform', 'lukewarm', 'cell', 'plywood'])
