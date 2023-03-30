import numpy as np
from PIL import ImageGrab
import cv2
import time

def process_img(image):
    org_img = image
    #gray scale image
    proccessed_img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    proccessed_img = cv2.Canny(proccessed_img, threshold1=200, threshold2=300)
    return proccessed_img

def screen_record(): 
    last_time = time.time()
    while(True):
        # 800x600 windowed mode
        screen =  np.array(ImageGrab.grab(bbox=(0,40,800,640)))
        print('loop took {} seconds'.format(time.time()-last_time))
        new_screen = process_img(screen)
        last_time = time.time()
        cv2.imshow('window',cv2.cvtColor(new_screen, cv2.COLOR_BGR2RGB))
        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break

def main():
    screen_record()

main()