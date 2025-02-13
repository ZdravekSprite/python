#python -m venv cpu
#.\cpu\Scripts\activate
#python.exe -m pip install --upgrade pip
#pip install opencv-python
import cv2 as cv
#pip install numpy
import numpy as np
#pip install pywin32
#from win32 import win32gui, win32ui, win32con
#from win32 import win32gui
#pip install Pillow
#from PIL import Image
#from time import sleep
#import os

from WindowMgr import WindowMgr

import numpy as np
import win32gui, win32ui, win32con
from PIL import Image
from time import sleep
import os
import re

class WindowCapture:

    def __init__ (self):
        """Constructor"""
        self._handle = None # hwnd
        self._handles = []
        self.w = 0
        self = 0

    def window_capture(self, wildcard):
        self.find_window_wildcard(wildcard)
        if not self._handle:
            raise Exception('Window not found: {}'.format(window_name))
        
        self.set_foreground()

        window_rect = win32gui.GetWindowRect(self._handle)
        self.w = window_rect[2] - window_rect[0]
        self.h = window_rect[3] - window_rect[1]

        border_pixels = 8
        titlebar_pixels = 30
        self.w = self.w - (border_pixels * 2)
        self.h = self.h - titlebar_pixels - border_pixels
        self.cropped_x = border_pixels
        self.cropped_y = titlebar_pixels

    def _window_enum_callback(self, hwnd, wildcard):
        """Pass to win32gui.EnumWindows() to check all the opened windows"""
        if re.match(wildcard, str(win32gui.GetWindowText(hwnd))) is not None:
            self._handles.append(hwnd)
            self._handle = hwnd
            
    def find_window_wildcard(self, wildcard):
        """find a window whose title matches the wildcard regex"""
        #self._handle = None
        #self._handles = []
        win32gui.EnumWindows(self._window_enum_callback, wildcard)

        self.set_handle()
    
    def set_foreground(self):
        """put the window in the foreground"""
        if self._handle != None:
            win32gui.SetForegroundWindow(self._handle)
        else:
            print("No handle is selected, couldn't set focus")

    def set_handle(self):
        """get one handle to operate on from all the matched handles"""
        if len(self._handles) < 1:
            print("Matched no window")
            return False

        if len(self._handles) > 1:
            print("Selecting the first handle of multiple windows:")
        else: # len(self._handles) == 1:
            print("Matched a single window:")

        self.print_matches()
        self._handle = self._handles[0]
        return True

    def print_matches(self):
        """print the title of each matched handle"""
        for hwnd in self._handles:
            print("- " + str(win32gui.GetWindowText(hwnd)))

    def get_screenshot(self):
        wDC = win32gui.GetWindowDC(self._handle)
        dcObj = win32ui.CreateDCFromHandle(wDC)
        cDC = dcObj.CreateCompatibleDC()
        dataBitMap = win32ui.CreateBitmap()
        dataBitMap.CreateCompatibleBitmap(dcObj, self.w, self.h)
        cDC.SelectObject(dataBitMap)
        cDC.BitBlt((0, 0), (self.w, self.h), dcObj, (self.cropped_x, self.cropped_y), win32con.SRCCOPY)

        signedIntsArray = dataBitMap.GetBitmapBits(True)
        #img = np.fromstring(signedIntsArray, dtype='uint8')
        img = np.frombuffer(signedIntsArray, dtype='uint8')
        img.shape = (self.h, self.w, 4)

        dcObj.DeleteDC()
        cDC.DeleteDC()
        win32gui.ReleaseDC(self._handle, wDC)
        win32gui.DeleteObject(dataBitMap.GetHandle())

        img = img[...,:3]
        img = np.ascontiguousarray(img) 
            
        return img

    def generate_image_dataset(self):
        if not os.path.exists("images"):
            os.mkdir("images")
        while(True):
            img = self.get_screenshot()
            im = Image.fromarray(img[..., [2, 1, 0]])
            im.save(f"./images/img_{len(os.listdir('images'))}.jpg")
            sleep(0.3)
            #sleep(0.3)
    
    def get_window_size(self):
        return (self.w, self.h)

if __name__ == "__main__":

    # Execute this cell to generate a dataset of images for the specified window.

    window_name = "OpenXcom Extended 7.15.0 (v2024-11-01)"
    wildcard_name = ".*OpenXcom.*"

    wincap = WindowCapture()
    wincap.window_capture(wildcard_name)
    print('test1')
    wincap.generate_image_dataset()
    print('test2')

    #w = WindowMgr()
    #w.find_window_wildcard(wildcard_name)
    #w.set_foreground()