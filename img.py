# -*- coding: utf-8 -*

from tkinter import *
import tkinter as tk
from PIL import Image, ImageTk
from tkinter import filedialog
import cv2
window = tk.Tk()
window.geometry("500x500")

def image():
    #initialdir 對話框開啟的目錄, title對話框的標題, filetypes找尋的副檔名
    img_path = filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("jpeg files","*.jpg"), ("png files","*.png"), ("gif files","*.gif"), ("all files","*.*")))
    img = cv2.cvtColor(cv2.resize(cv2.imread(img_path), (480, 315)), cv2.COLOR_BGR2RGB)
    #Image.fromarray 將陣列轉為圖像
    img = ImageTk.PhotoImage(Image.fromarray(img))
    image_canvas.create_image(0,0,anchor = NW, image = img)
    image_canvas.img = img
#建立canvas 顯示圖片
image_canvas = tk.Canvas(window, bg = '#333f50',height = 315, width = 480)
image_canvas.place(x = 10, y = 5)
#建立讀取讀片按鈕  
button = tk.Button(window, text = "引入檔案", width = 10, height = 2, command = image)
button.place(x = 420, y = 465)
window.mainloop()