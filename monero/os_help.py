import os

def path(file):
    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
    return os.path.sep.join([SCRIPT_DIR, file])

def file_del(file, debug=False):
    if os.path.exists(file):
        os.remove(file)
        print(f"{file} deleted")
    else:
        if debug: print(f"{file} does not exist")
        pass

def file_read(file):
    if os.path.exists(path(file)):
        return open(path(file),"r",encoding="utf-8")
    else:
        print(f"{file} does not exist")
        pass

def isWin():
    if os.name != 'posix':
        print(os.name)
        #runcmd("dir")
        return True
    else:
        print(os.uname())
        return False