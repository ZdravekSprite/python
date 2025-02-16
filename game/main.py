#pip install pyautogui
from pyautogui import *
import pyautogui
import time
#import keyboard
#import numpy as np
#import random
import win32api, win32con

import os
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

def click(x,y):
    win32api.SetCursorPos((x,y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
    time.sleep(0.1)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)

def displayMousePosition():
    pyautogui.displayMousePosition()


def selectGUI(png):
    try:
        box = pyautogui.locateOnScreen(os.path.sep.join([SCRIPT_DIR, png]), grayscale=True, confidence=0.8)
        print(png,box)
        click(int(box.left+box.width/2),int(box.top+box.height/2))
        time.sleep(0.5)
        return True
    except:
        print("No",png)
        return False

if __name__ == "__main__":
    print(__file__)

    time.sleep(2)
    #displayMousePosition()
    for png in ['new','super','ok','loc']:
        selectGUI(png+'.png')
