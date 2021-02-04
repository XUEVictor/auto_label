# -*- coding: utf-8 -*
import tkinter as tk
import cv2
from PIL import Image,ImageTk
from UI import UI
from extract import extract_obj
import numpy as np
from hsv import HSV

def crop_grab(img,roi):
    (x, y) = (roi[0], roi[1])
    (w, h) = (roi[2], roi[3])
    return img[y:y+h, x:x+w]

if __name__ == "__main__":




    obj_name = 'cookie'
    img1_bg = cv2.imread('WIN_20210201_19_39_35_Pro.jpg')
    img_obj = cv2.imread('cookie.jpg')
    
    hsv = HSV()
    eo = extract_obj(obj_name,obj_name)
    mask1 ,roi_,dst = eo.GetMask(img_obj)
    dst_crop = hsv.crop(img_obj,roi_)
    mask1_crop = hsv.crop(mask1,roi_)

    for i in range(100):
        img3 = eo.exec(img1_bg,dst_crop,mask1_crop)
        cv2.imshow('img3',img3)
        cv2.waitKey(300)




    # eo.exec(img)
    # root = tk.Tk()
    # ui = UI(root)
    # root.mainloop()
    # cv2.destroyAllWindows()
