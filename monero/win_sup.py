import subprocess
from subprocess import PIPE, STDOUT
from config import *
from os_help import file_del, path

def callcmd(commandList, shell=True):
    print(commandList)
    subprocess.call(commandList, shell=shell)

def runcmd(commandList):
    print(commandList)
    result = subprocess.run(commandList, shell=True, capture_output=True, text=True)
    print(result.stdout)

def with_popen(commandList):
    with subprocess.Popen(commandList, stdin=PIPE, stdout=PIPE, text=True) as proc:
        '''
        print('write1')
        proc.stdin.write('\n')
        print('write2')
        proc.stdin.write('test\n')
        print('write3')
        proc.stdin.write('test\n')
        print('write4')
        proc.stdin.write('N\n')
        '''
        try:
            print('comunicate1',proc.pid)
            outs, errs = proc.communicate('\r\n',timeout=15)
        except subprocess.TimeoutExpired:
            print('except1')
            proc.stdout.flush()
            print('flush1')
            try:
                print('comunicate2',proc.pid)
                outs, errs = proc.communicate('N\r\n',timeout=15)
            except subprocess.TimeoutExpired:
                print('except2')
                proc.kill()
                outs, errs = proc.communicate()
        print(outs)

if __name__ == '__main__':
    print(__file__)
    file_del(path("test"))
    file_del(path("test.keys"))
    file_del(path("monero-wallet-cli.log"))
    #callcmd(monerod_path)
    #callcmd(monero_wallet_cli_path)
    program = monero_wallet_cli_path
    argument1 = "--restore-deterministic-wallet"
    argument2 = "--generate-new-wallet=monero/test"
    argument3 = "--restore-height=3388000"
    argument4 = "--password=test"
    commandList = [program, argument1, test_argument, argument2, argument3, argument4] # commandLine
    #print(commandList)
    #callcmd(commandList)
    #with_popen(commandList)
