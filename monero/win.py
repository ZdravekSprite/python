#monerod.exe
#C:\ProgramData\bitmonero

import subprocess
from subprocess import PIPE, STDOUT
from config import argument2
from os_help import file_del, path, isWin

def create_wallet():
    file_del('monero/test')
    file_del('monero/test.keys')
    file_del('monero/monero-wallet-cli.log')
    program = path("monero-wallet-cli.exe")
    argument1 = "--restore-deterministic-wallet"
    argument3 = "--generate-new-wallet=monero/test"
    argument4 = "--restore-height=3378000"
    #commandList = [program, argument1] # commandLine
    commandList = [program, argument1, argument2, argument3, argument4] # commandLine
    #result = subprocess.run(commandList, shell=True, capture_output=True, text=True)
    #print(result.stdout)
    #ps = subprocess.Popen(commandList , shell=False, stdin=PIPE, stdout=PIPE, stderr=STDOUT)
    #print(ps)
    subprocess.call(commandList, shell=True) #Run under Windows

def runcmd(cmd):
    result = subprocess.run([cmd], shell=True, capture_output=True, text=True)
    print(result.stdout)


if __name__ == '__main__':
    print(__file__)
    if isWin:
        #runcmd("dir")
        create_wallet()
