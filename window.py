import numpy as np
from PIL import ImageGrab
import cv2
import time
import ctypes
import ctypes.wintypes
from directkeys import PressKey, ReleaseKey, W, A, S, D

def roi(img, vertices):
    #blank mask
    mask = np.zeros_like(img)

    #fill the mask
    cv2.fillPoly(mask, [vertices], 255)

    # now only show area that is the mask (the road in this case)
    masked = cv2.bitwise_and(img, mask)
    return masked

def draw_lines(img, lines):
    try:
        for line in lines:
            cords = line[0]
            #x1, x2, y1, y2, color, thickness
            cv2.line(img, (cords[0], cords[1]), (cords[2], cords[3]), [255, 255, 255], 3)
    except:
        pass
    

# retrieve edges of image via grayscale and canny edge detection
def process_img(image):
    #gray scale image
    proccessed_img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    proccessed_img = cv2.Canny(proccessed_img, threshold1=200, threshold2=300)
    vertices = np.array([[10, 500], [10, 300], [300, 200], [500, 200], [800, 300], [800, 500]], np.int32)

    # add gaus blur to improve line detection
    proccessed_img = cv2.GaussianBlur(proccessed_img,(5,5),0)
    proccessed_img = roi(proccessed_img, vertices)

    # coordinates of lines detected from the canny edge detection
    lines = cv2.HoughLinesP(proccessed_img, 1, np.pi/180, 180, 20, 15)
    # draw lines on image
    draw_lines(proccessed_img, lines)
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

        print('Loop took {} seconds'.format(time.time()-last_time))
        last_time = time.time()
        new_screen = process_img(screen)
        last_time = time.time()
        cv2.imshow('window', new_screen)
        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break

main()