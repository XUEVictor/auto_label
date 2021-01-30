
# -*- coding: utf-8 -*
import tkinter
import tkinter.simpledialog
import tkinter.colorchooser
import tkinter.filedialog
import cv2
from PIL import Image,ImageTk
import os
import glob
class UI:
    root = None
    cb = None
    lastDraw = 0
    end=[0]

    def __init__(self,root):
        self.root = root
        self.cb = callback(self)
        self.init_ui(self.root)

        self.update_img(self.cb.Img)
        # cv2.imshow('self.cb.Img',self.cb.Img)
        # cv2.waitKey()
    def update_img(self,img):
        if img is not None:
            cv2image = cv2.cvtColor(img, cv2.COLOR_BGR2RGBA)
            current_image = Image.fromarray(cv2image)
            imgtk = ImageTk.PhotoImage(image=current_image)
            self.image_canvas.create_image(640 + 50,360 + 50, image = imgtk)
            self.image_canvas.img = imgtk

    def init_ui(self,root):
        root.title("opencv + tkinter")
        # 定義視窗大小
        self.center_window(root,1280 + 300,720 + 300)
        # 創建一個canvas
        self.image_canvas = tkinter.Canvas(root, bg = '#333f50',height = 820, width = 1380)
        self.image_canvas.pack(padx=10, pady=10)
        self.image_canvas.bind('<B1-Motion>', onLeftButtonMove)  #按住并移动左键
        self.image_canvas.bind('<ButtonRelease-1>', onLeftButtonUp)  #释放左键
        self.image_canvas.bind('<ButtonRelease-3>', onRightButtonUp) #释放右键
        root.config(cursor="arrow")
        tkinter.Button(root, text="Next >>", command=self.cb.btn_Next).pack(side='right', ipadx=20, padx=30)
        tkinter.Button(root, text="<< Prev", command=self.cb.btn_Prev).pack(side='left', ipadx=20, padx=30)
    
    def center_window(self,app, w, h):
        ws = app.winfo_screenwidth()
        hs = app.winfo_screenheight()
        app.geometry('%dx%d' % (w, h))

class callback:
    Img = None
    ui = None
    Funct = None
    Img_List = []
    counter = 0
    # 建構式
    def __init__(self,ui):
        self.ui = ui
        self.Funct = Function()
        self.Img_List = self.Funct.read_direct_img('img')
        self.Img = self.Img_List[0]


    def btn_Next(self):
        if(self.counter + 1 < len(self.Img_List)):
            self.counter = self.counter + 1
            print('press Next')
            self.Img = self.Img_List[self.counter]
            self.ui.update_img(self.Img)
        else:
            print('No Next')
    def btn_Prev(self):
        if(self.counter - 1 > 0):
            self.counter = self.counter - 1
            print('press Prev')
            self.Img = self.Img_List[self.counter]
            self.ui.update_img(self.Img)
        else:
            print('No prev')
class Function:
    array_of_img = [] # this if for store all of the image data
    
    def __init__(self):
        pass

    # this function is for read image,the input is directory name
    def read_direct_img(self,directory_name):
        # this loop is for read each image in this foder,directory_name is the foder name with images.
        filelist = os.listdir(r"./"+directory_name)
        # filelist.sort(key=int)
        filelist.sort()
        for filename in filelist :
            # print(filename) #just for test
            #img is used to store the image data 
            img = cv2.imread(directory_name + "/" + filename)
            self.array_of_img.append(img)
        # print(len(self.array_of_img))
        return self.array_of_img
