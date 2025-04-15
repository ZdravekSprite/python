class Injector:
    '''Class that allows running arbitrary Python code in any process'''
  
    def initialize(self):
        '''Calls Py_InitializeEx(0) in the remote process'''
        ...
      
    def finalize(self):
        '''Calls Py_FinalizeEx(0) in the remote process'''
        ...
  
    def run_code(self, source_code, should_wait=False):
        '''Runs the Python source code in the remote process in a separate thread'''
        ...

import win32api, win32con
def msg_box(msg="hello win32api"):
    win32api.MessageBox(0, msg, "win32api", win32con.MB_OK)

#pip install WMI
import wmi
def get_disk_space():
    conn = wmi.WMI ()
    for disk in conn.Win32_LogicalDisk():
        if disk.size != None:
            print(disk.Caption, "is {0:.2f}% free".format(100*float(disk.FreeSpace)/float(disk.Size)))
        
if __name__ == '__main__':
    print(__file__)
    msg_box()
    get_disk_space()
