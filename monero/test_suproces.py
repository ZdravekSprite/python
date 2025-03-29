import subprocess

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

if __name__ == '__main__':
    print(__file__)
    test2()