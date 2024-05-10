import copy
import sys

import numpy as np
import win32gui, win32ui, win32con
import time
from PIL import Image
import math

class WindowCapture:

    # properties
    w = 0
    h = 0
    hwnd = None

    # constructor
    def __init__(self, window_name):
        pass


    def get_screenshot_2(self):
        hwnd_target = self.get_sot_hwnd()#0x30dbe # Try SOT?

        left, top, right, bot = win32gui.GetWindowRect(hwnd_target)
        w = right - left
        h = bot - top

        window_rect = win32gui.GetWindowRect(hwnd_target)
        w = window_rect[2] - window_rect[0]
        w = 3840
        h = window_rect[3] - window_rect[1]
        h = 2160
        left = 0
        top = 0 #keep top and height in total

        #only grab middle of screen?
        left = int(math.floor(w/4))
        #top = int(math.floor(h/4))
        w = int(int(math.floor(w/4))*3)
        #h = int(math.floor(h/2))

        #win32gui.SetForegroundWindow(hwnd_target)
        #time.sleep(1.0)

        hdesktop = win32gui.GetDesktopWindow()
        hwndDC = win32gui.GetWindowDC(hdesktop)
        mfcDC = win32ui.CreateDCFromHandle(hwndDC)
        saveDC = mfcDC.CreateCompatibleDC()

        saveBitMap = win32ui.CreateBitmap()
        saveBitMap.CreateCompatibleBitmap(mfcDC, w, h)

        saveDC.SelectObject(saveBitMap)

        result = saveDC.BitBlt((0, 0), (w, h), mfcDC, (left, top), win32con.SRCCOPY)

        bmpinfo = saveBitMap.GetInfo()
        bmpstr = saveBitMap.GetBitmapBits(True)


        im = Image.frombuffer(
            'RGB',
            (bmpinfo['bmWidth'], bmpinfo['bmHeight']),
            bmpstr, 'raw', 'BGRX', 0, 1)

        im_grey = copy.deepcopy(im)

        #im = im.convert('1') #THIS converts to 0-255 black white

        white_threshold = 200
        fn = lambda  x : 0 if x > white_threshold else 255
        im = im.convert('L').point(fn, mode='1')
        im_grey = im_grey.convert('L')


        win32gui.DeleteObject(saveBitMap.GetHandle())
        saveDC.DeleteDC()
        mfcDC.DeleteDC()
        win32gui.ReleaseDC(hdesktop, hwndDC)

        return im, im_grey

    # find the name of the window you're interested in.
    # once you have it, update window_capture()
    # https://stackoverflow.com/questions/55547940/how-to-get-a-list-of-the-name-of-every-open-window
    def list_window_names(self):
        def winEnumHandler(hwnd, ctx):
            if win32gui.IsWindowVisible(hwnd):
                print(hex(hwnd), win32gui.GetWindowText(hwnd))
        win32gui.EnumWindows(winEnumHandler, None)

    def get_sot_hwnd(self):
        return win32gui.FindWindow(None, "Sea of Thieves")
