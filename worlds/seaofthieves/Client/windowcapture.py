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
    # cropped_x = 0
    # cropped_y = 0
    # offset_x = 0
    # offset_y = 0

    # constructor
    def __init__(self, window_name):
        pass
        # # find the handle for the window we want to capture
        # self.hwnd = win32gui.FindWindow(None, window_name)
        # #if not self.hwnd:
        # #    raise Exception('Window not found: {}'.format(window_name))
        #
        # # get the window size
        # window_rect = win32gui.GetWindowRect(self.hwnd)
        # self.w = window_rect[2] - window_rect[0]
        # self.h = window_rect[3] - window_rect[1]
        #
        # # account for the window border and titlebar and cut them off
        # border_pixels = 8
        # titlebar_pixels = 30
        # self.w = self.w - (border_pixels * 2)
        # self.h = self.h - titlebar_pixels - border_pixels
        # self.cropped_x = border_pixels
        # self.cropped_y = titlebar_pixels
        #
        # # set the cropped coordinates offset so we can translate screenshot
        # # images into actual screen positions
        # self.offset_x = window_rect[0] + self.cropped_x
        # self.offset_y = window_rect[1] + self.cropped_y

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
        w = int(math.floor(w/2))
        #h = int(math.floor(h/2))

        win32gui.SetForegroundWindow(hwnd_target)
        time.sleep(1.0)

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

        #im = im.convert('1') #THIS converts to 0-255 black white
        white_threshold = 200
        fn = lambda  x : 0 if x > white_threshold else 255
        im = im.convert('L').point(fn, mode='1')


        win32gui.DeleteObject(saveBitMap.GetHandle())
        saveDC.DeleteDC()
        mfcDC.DeleteDC()
        win32gui.ReleaseDC(hdesktop, hwndDC)

        return im
    # def get_screenshot(self):
    #
    #     # get the window image data
    #     wDC = win32gui.GetWindowDC(self.hwnd)
    #     dcObj = win32ui.CreateDCFromHandle(wDC)
    #     cDC = dcObj.CreateCompatibleDC()
    #     dataBitMap = win32ui.CreateBitmap()
    #     dataBitMap.CreateCompatibleBitmap(dcObj, self.w, self.h)
    #     cDC.SelectObject(dataBitMap)
    #     cDC.BitBlt((0, 0), (self.w, self.h), dcObj, (self.cropped_x, self.cropped_y), win32con.SRCCOPY)
    #
    #     # convert the raw data into a format opencv can read
    #     #dataBitMap.SaveBitmapFile(cDC, 'debug.bmp')
    #     signedIntsArray = dataBitMap.GetBitmapBits(True)
    #     img = np.fromstring(signedIntsArray, dtype='uint8')
    #     img.shape = (self.h, self.w, 4)
    #
    #     # free resources
    #     dcObj.DeleteDC()
    #     cDC.DeleteDC()
    #     win32gui.ReleaseDC(self.hwnd, wDC)
    #     win32gui.DeleteObject(dataBitMap.GetHandle())
    #
    #     # drop the alpha channel, or cv.matchTemplate() will throw an error like:
    #     #   error: (-215:Assertion failed) (depth == CV_8U || depth == CV_32F) && type == _templ.type()
    #     #   && _img.dims() <= 2 in function 'cv::matchTemplate'
    #     #img = img[...,:3]
    #
    #     # make image C_CONTIGUOUS to avoid errors that look like:
    #     #   File ... in draw_rectangles
    #     #   TypeError: an integer is required (got type tuple)
    #     # see the discussion here:
    #     # https://github.com/opencv/opencv/issues/14866#issuecomment-580207109
    #     #img = np.ascontiguousarray(img)
    #
    #     return img

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

    # translate a pixel position on a screenshot image to a pixel position on the screen.
    # pos = (x, y)
    # WARNING: if you move the window being captured after execution is started, this will
    # return incorrect coordinates, because the window position is only calculated in
    # the __init__ constructor.
    # def get_screen_position(self, pos):
    #     return (pos[0] + self.offset_x, pos[1] + self.offset_y)