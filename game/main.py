#pip install pyautogui
from pyautogui import *
import pyautogui
import time
#pip install keyboard
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
    pyautogui.moveTo(0,0)
    try:
        box = pyautogui.locateOnScreen(os.path.sep.join([SCRIPT_DIR, 'img', png]), grayscale=True, confidence=0.8)
        print(png,box)
        click(int(box.left+box.width/2),int(box.top+box.height/2))
        time.sleep(0.3)
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
        pyautogui.typewrite('Grcka')
        for png in ['ok2']:
            selectGUI(png+'.png')
    if selectGUI('lift.png'):
        print(position())
    if selectGUI('hangar0.png'):
        selectGUI('hangar1.png')
        #print(position())
    if selectGUI('hangar0.png'):
        selectGUI('hangar2.png')
        #print(position())
    if selectGUI('hangar0.png'):
        selectGUI('hangar3.png')
        #print(position())
    if selectGUI('life0.png'):
        selectGUI('life1.png')
        #print(position())
    if selectGUI('radar0.png'):
        selectGUI('radar1.png')
        #print(position())
    if selectGUI('warehouse0.png'):
        selectGUI('warehouse1.png')
        #print(position())
    if selectGUI('lab0.png'):
        selectGUI('lab1.png')
        #print(position())
    if selectGUI('work0.png'):
        selectGUI('work1.png')
        #print(position())

def getSol():
    for png in ['base0','sol0']:
        selectGUI(png+'.png')
        #print(position())
    if selectGUI('sol1.png'):
        #print(position())
        solRot()

def solRot():
    start = getStart()
    rows = getRows()
    exit = False
    if start:
        for n in range(8):
            stats = getStats(start,rows)
            if stats['row1']<55:
                exit = True
            #if stats['row6']<55:
            #    exit = True
            print(stats)
            if not exit:
                if not selectGUI('next.png'):
                    selectGUI('next1.png')
            else:
                break
    if exit:
        exitStats()
        newGame()
        getSol()

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

def exitStats():
    selectGUI('ok1.png')
    selectGUI('ok1.png')
    selectGUI('geoscape.png')
    selectGUI('options.png')
    selectGUI('exit.png')
    selectGUI('yes.png')

def getStats(start,rows):
    stats = {}
    for no in [10]+list(range(20,72))+[73,74,75,76,77,79]:
        png = str(no)+'.png'
        try:
            box = pyautogui.locateAllOnScreen(os.path.sep.join([SCRIPT_DIR, png]), grayscale=True, confidence=0.99)
            for b in box:
                #print(png,b.top,rows[selectRow(start,b.top)])
                stats[rows[selectRow(start,b.top)]] = no
        except:
            #print("No",png)
            pass
    #for r in rows:
    #    print (r,stats[r])
    return stats

if __name__ == "__main__":
    print(__file__)

    time.sleep(1)
    newGame()
    getSol()
    #solRot()
    #exitStats()
