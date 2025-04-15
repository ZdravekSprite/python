import subprocess
from subprocess import PIPE, STDOUT
from config import monerod_path, monero_wallet_cli_path, test_argument
from os_help import file_del, path

import time
#pip install keyboard
#import keyboard
import win32api, win32con

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

def muzika():
    A = 55
    B = 62
    C = 65
    D = 73
    E = 82
    F = 87
    G = 98
    QUARTER = 400
    HALF = QUARTER*2
    song = [(C, QUARTER), (C, QUARTER), (G, QUARTER), (G, QUARTER), (A, QUARTER), (A, QUARTER), (G, HALF) ]
    for note, length in song:
        win32api.Beep(note, length)

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
    #time.sleep(1)
    #muzika()
    win32api.WinExec("notepad", win32con.SW_SHOWMAXIMIZED)
