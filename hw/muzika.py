import time
#pip install pypiwin32
import win32api, win32con

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
    time.sleep(1)
    muzika()
    win32api.WinExec("notepad", win32con.SW_SHOWMAXIMIZED)
