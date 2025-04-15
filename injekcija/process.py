import wmi # to get the target process pid by name
import os # for spinning up processes to inject on-demand    
import threading # for spinning up processes to inject on-demand
from time import sleep

'''
'Caption','CommandLine','CreationClassName','CreationDate','CSCreationClassName',
'CSName','Description','ExecutablePath','ExecutionState','Handle','HandleCount','InstallDate',
'KernelModeTime','MaximumWorkingSetSize','MinimumWorkingSetSize','Name','OSCreationClassName',
'OSName','OtherOperationCount','OtherTransferCount','PageFaults','PageFileUsage',
'ParentProcessId','PeakPageFileUsage','PeakVirtualSize','PeakWorkingSetSize','Priority',
'PrivatePageCount','ProcessId','QuotaNonPagedPoolUsage','QuotaPagedPoolUsage',
'QuotaPeakNonPagedPoolUsage','QuotaPeakPagedPoolUsage','ReadOperationCount','ReadTransferCount','SessionId',
'Status','TerminationDate','ThreadCount','UserModeTime','VirtualSize','WindowsVersion',
'WorkingSetSize','WriteOperationCount','WriteTransferCount'
'''

def get_proc_id(process_name):
    processes = wmi.WMI().Win32_Process(name=process_name)
    if len(processes):
        pid = processes[0].ProcessId
        print(f"[*] {process_name} process id: {pid}")
        print(processes[0].CommandLine)
        return int(pid)
    else:
        print(f"[*] No {process_name}")

def start_process(process_name):
    print(f'[*] starting {process_name}')
    return os.system(process_name)
    s = threading.Thread(target=start_process)
    s.start()
    sleep(2)

def all_procesess():
    all_procesess = wmi.WMI().Win32_Process()
    for p in all_procesess:
        print(f"[*] {p.name} process id: {p.ProcessId}")
    return all_procesess

def get_process(cmd_line):
    name = cmd_line.split(" ")[0].split("\\")[-1]
    processes = wmi.WMI().Win32_Process(name=name)
    if len(processes):
        pid = processes[0].ProcessId
        print(f"[*] {processes[0].Description} | process id: {pid} | cmd: {processes[0].CommandLine}")
        return int(pid)
    else:
        print(f"[*] No {cmd_line}")

# start target service
def start_service(target):
    conn = wmi.WMI()
    for s in conn.Win32_Service(StartMode="Auto", State="Stopped"):
        if 'Update' in s.Name:
            result, = s.StartService()
            if result == 0: print("Successfully started service:", s.Name)

if __name__ == '__main__':
    print(__file__)
    #if not start_process('calc'):
    #    get_proc_id("CalculatorApp.exe")
