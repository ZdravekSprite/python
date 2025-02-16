#pip install pyautogui
from pyautogui import *
import pyautogui
import time
#pip install keyboard
import keyboard
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
def newGame():
    for png in ['new','super','ok1']:
        selectGUI(png+'.png')
    #displayMousePosition()
    buildBase()

def buildBase():
    if selectGUI('loc.png'):
        pyautogui.typewrite('Base')
        for png in ['ok2']:
            selectGUI(png+'.png')
    if selectGUI('lift.png'):
        print(position())
    if selectGUI('hangar0.png'):
        selectGUI('hangar1.png')
        print(position())
    if selectGUI('hangar0.png'):
        selectGUI('hangar2.png')
        print(position())
    if selectGUI('hangar0.png'):
        selectGUI('hangar3.png')
        print(position())
    if selectGUI('life0.png'):
        selectGUI('life1.png')
        print(position())
    if selectGUI('radar0.png'):
        selectGUI('radar1.png')
        print(position())
    if selectGUI('warehouse0.png'):
        selectGUI('warehouse1.png')
        print(position())
    if selectGUI('lab0.png'):
        selectGUI('lab1.png')
        print(position())
    if selectGUI('work0.png'):
        selectGUI('work1.png')
        print(position())

def getSol():
    if selectGUI('base0.png'):
        print(position())
    if selectGUI('sol0.png'):
        print(position())
    if selectGUI('sol1.png'):
        print(position())
    solRot()

def solRot():
    start = getStart()
    rows = getRows()
    if start:
        for n in range(8):
            getStats(start,rows)
            selectGUI('next.png')

def getRows():
        rows = []
        for no in range(9):
            r = 'row'+str(no+1)
            rows.append(r)
            """
            try:
                box = pyautogui.locateOnScreen(os.path.sep.join([SCRIPT_DIR, r+'.png']), grayscale=True, confidence=0.99)
                print(r,box.top)
            except:
                print("No",r)
            """
        return rows

def getStart():
    try:
        box = pyautogui.locateOnScreen(os.path.sep.join([SCRIPT_DIR, 'row1.png']), grayscale=True, confidence=0.99)
        start = box.top + 10
        #print('start',start)
        return start
    except:
        print("No start")
        return False

def selectRow(start:int,line:int):
    for r in range(9):
        if line < start + r * 21.875:
            return r

def getStats(start,rows):
        stats = {}
        for no in [10]+list(range(20,72))+[73,75,77,79]:
            png = str(no)+'.png'
            try:
                box = pyautogui.locateAllOnScreen(os.path.sep.join([SCRIPT_DIR, png]), grayscale=True, confidence=0.99)
                for b in box:
                    #print(png,b.top,rows[selectRow(start,b.top)])
                    stats[rows[selectRow(start,b.top)]] = no
            except:
                #print("No",png)
                pass
        for r in rows:
            print (r,stats[r])

if __name__ == "__main__":
    print(__file__)

    time.sleep(1)
    #newGame()
    #getSol()
    solRot()
