import subprocess
import sys

def test1():
    subprocess.call("dir", shell=True) #Run under Windows

def test2():
    command1 = subprocess.Popen(['dir'],
                        shell=True,
                        stdout=subprocess.PIPE,
                        )
    command2 = subprocess.Popen(['findstr', 'py'],
                        stdin=command1.stdout,
                        shell=True,
                        stdout=subprocess.PIPE,
                        )
    end_of_pipe = command2.stdout
    for line in end_of_pipe:    
        print('\t', line.strip())

def test3():
    proc = subprocess.Popen(['ping', '18.8.8.8', '-t'],
                            shell=True,
                            stdout=subprocess.PIPE,
                            )
    while True: # Infinite loop
        output = proc.stdout.readline()
        if proc.poll() is not None:
            break    
        if output:
            print('o:',output.strip())

def test4():
    print('One line at a time:')
    proc = subprocess.Popen('python hw\\repeater.py', 
                            shell=True,
                            stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE,
                            )
    for i in range(10):
        proc.stdin.write(b'%d\n' % i)
        output = proc.stdout.readline()
        print(output.rstrip())
        #print('%d' % i)
    remainder = proc.communicate()[0]
    print(remainder)

def test5():
    print('All output at once:')
    proc = subprocess.Popen('python hw\\repeater.py', 
                            shell=True,
                            stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE,
                            )
    for i in range(10):
        proc.stdin.write(b'%d\n' % i)

    output = proc.communicate()[0]
    print(output)

if __name__ == '__main__':
    print(__file__)
    test5()