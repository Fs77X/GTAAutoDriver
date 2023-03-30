import numpy as np
from PIL import ImageGrab
import cv2
import time
import ctypes
import ctypes.wintypes

# retrieve edges of image via grayscale and canny edge detection
def process_img(image):
    #gray scale image
    proccessed_img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    proccessed_img = cv2.Canny(proccessed_img, threshold1=200, threshold2=300)
    return proccessed_img

# https://stackoverflow.com/questions/7142342/get-window-position-size-with-python# thanks to ShortArrow's answer!
# Simple function to retrieve window coordinates of GTA V
def GetWindowRectFromName(name:str)-> tuple:
    hwnd = ctypes.windll.user32.FindWindowW(0, name)
    rect = ctypes.wintypes.RECT()
    ctypes.windll.user32.GetWindowRect(hwnd, ctypes.pointer(rect))
    return (rect.left, rect.top, rect.right, rect.bottom)

def main():
    last_time = time.time()
    while(True):
        window_name = "Grand Theft Auto V"
        # retrieve cords
        cords = GetWindowRectFromName(window_name)
        
        screen =  np.array(ImageGrab.grab(bbox=cords))

        #capture only game and not the entire window
        h, w, _ = screen.shape
        screen = screen[h - 600:, w - 800:, ]

        print('loop took {} seconds'.format(time.time()-last_time))
        new_screen = process_img(screen)
        last_time = time.time()
        cv2.imshow('window',cv2.cvtColor(screen, cv2.COLOR_BGR2RGB))
        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break

main()