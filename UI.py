
# -*- coding: utf-8 -*
import tkinter
import tkinter.simpledialog
import tkinter.colorchooser
import tkinter.filedialog
import cv2
import os
import glob
import sys


from PIL import Image,ImageTk
from gen_xml import xml
from hsv import HSV

class UI:
    root = None
    cb = None
    Size_w = 1280
    Size_h = 720
    expand_w = 100
    expand_h = 100

    

    def __init__(self,root):
        self.root = root
        self.cb = callback(self)
        self.init_ui(self.root)
        self.update_img(self.cb.Img)

    def update_img(self,img):
        if img is not None:
            cv2image = cv2.cvtColor(img, cv2.COLOR_BGR2RGBA)
            current_image = Image.fromarray(cv2image)
            imgtk = ImageTk.PhotoImage(image=current_image)
            print((img.shape[1]/2,img.shape[0]/2))
            self.image_canvas.create_image(img.shape[1]/2,img.shape[0]/2, image = imgtk)
            self.image_canvas.img = imgtk

    def init_ui(self,root):
        # 圖片大小
        w = self.cb.Img.shape[1]
        h = self.cb.Img.shape[0]
        print('w,h',(w,h))

        root.title("opencv + tkinter")
        # 定義視窗大小
        self.center_window(root,self.Size_w + self.expand_w,self.Size_h + self.expand_h)
        # 創建一個canvas
        self.image_canvas = tkinter.Canvas(root, bg = '#333f50',height = h , width = w)
        paint = Painter(self.image_canvas,tkinter)
        self.cb.painter = paint
        self.cb.painter.img = self.cb.Img

        self.image_canvas.pack(padx=10, pady=10)
        self.image_canvas.bind('<Button-1>', paint.onLeftButtonDown)  #单击左键
        self.image_canvas.bind('<B1-Motion>', paint.onLeftButtonMove)  #按住并移动左键
        self.image_canvas.bind('<ButtonRelease-1>', paint.onLeftButtonUp)  #释放左键
        self.image_canvas.bind('<ButtonRelease-3>', paint.onRightButtonUp) #释放右键
        root.config(cursor="arrow")
        tkinter.Button(root, text="Next >>", command=self.cb.btn_Next).pack(side='right', ipadx=20, padx=30)
        tkinter.Button(root, text="<< Prev", command=self.cb.btn_Prev).pack(side='left', ipadx=20, padx=30)
    
    def center_window(self,app, w, h):
        ws = app.winfo_screenwidth()
        hs = app.winfo_screenheight()
        app.geometry('%dx%d' % (w, h))

class callback:
    Img = None
    Img_Name = None
    ui = None
    Funct = None
    Img_List = []
    Img_Name_List = []
    counter = 0
    painter = None
    # 建構式
    def __init__(self,ui):
        self.ui = ui
        self.Funct = Function()
        self.Img_List,self.Img_Name_List = self.Funct.read_direct_img('img/' + sys.argv[1] + '/')
        self.Img = self.Img_List[0]
        self.Img_Name = self.Img_Name_List[0]
        self.xml = xml()
    def btn_Next(self):
        if(self.counter + 1 < len(self.Img_List)):
            print('press Next')
            targefile = sys.argv[1]
            Type = sys.argv[2]
            start_num = sys.argv[3]
            if(len(self.painter.record_rect) > 0):
                # print('record_rect[0]',self.painter.record_rect[0])
                # self.Img_Name = self.Img_Name.split(".", 1)[0]
                # print('Img_Name',self.Img_Name)
                Name = str(int(start_num) + self.counter)
                # hsv = HSV()
                # hsv.find_roi(self.Img,self.painter.record_rect[0])

                self.xml.makexml(targefile,Name,Type,self.Img,self.painter.record_rect[0])

            self.counter = self.counter + 1

            self.Img = self.Img_List[self.counter]
            self.Img_Name = self.Img_Name_List[self.counter]

            self.ui.update_img(self.Img)
            self.painter.Draw_rect()
            self.painter.img = self.Img

        else:
            print('No Next')
    def btn_Prev(self):
        if(self.counter - 1 > 0):
            self.counter = self.counter - 1
            print('press Prev')

            targefile = sys.argv[1]
            Type = sys.argv[2]
            start_num = sys.argv[3]
            if(len(self.painter.record_rect) > 0):
                Name = str(int(start_num) + self.counter)
                # hsv = HSV()
                # hsv.find_roi(self.Img,self.painter.record_rect[0])
                self.xml.makexml(targefile,Name,Type,self.Img,self.painter.record_rect[0])

            self.counter = self.counter + 1

            self.Img = self.Img_List[self.counter]
            self.Img_Name = self.Img_Name_List[self.counter]

            self.ui.update_img(self.Img)
            self.painter.Draw_rect()
            self.painter.img = self.Img
        else:
            print('No prev')

class Function:
    array_of_img = [] # this if for store all of the image data
    file_name = []
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
            self.file_name.append(filename)
        # print(len(self.array_of_img))
        return self.array_of_img,self.file_name

class Painter:
    lastDraw = None
    canvas = None
    foreColor = '#00DB00'
    end=[0]
    record_rect = []
    img = None
    
    def __init__(self,canvas,tkinter):
        self.canvas = canvas
        self.what = tkinter.IntVar(value=3)
        self.yesno = tkinter.IntVar(value=0)
        self.X = tkinter.IntVar(value=0)
        self.Y = tkinter.IntVar(value=0)
        self.menu = tkinter.Menu(self.canvas, tearoff=0)
        self.menu.add_command(label='清除', command=self.Clear)

        pass
    #按下滑鼠允許畫圖
    def onLeftButtonDown(self,event):
        self.yesno.set(1)
        self.X.set(event.x)
        self.Y.set(event.y)

        if self.what.get()==4:
            self.canvas.create_text(event.x, event.y, font=("微软雅黑", int(size)),text=text,fill=foreColor)
            self.what.set(1)

    #按住移動,畫圖
    def onLeftButtonMove(self,event):
        if self.yesno.get()==0:
            return
        if self.what.get()==3:
            #畫矩形
            try:
                self.canvas.delete(self.lastDraw)
            except Exception as e:
                pass

            self.lastDraw = self.canvas.create_rectangle(self.X.get(), self.Y.get(), event.x, event.y,
                                                outline=self.foreColor,width=3)
    #滑鼠抬起,不能畫圖
    def onLeftButtonUp(self,event):
        if self.what.get()==3:
            self.lastDraw=self.canvas.create_rectangle(self.X.get(), self.Y.get(), event.x, event.y,  outline=self.foreColor,width=3)
            self.record_rect.append([self.X.get(), self.Y.get(), event.x, event.y])

        self.yesno.set(0)
        self.end.append(self.lastDraw)

    #鼠标右键抬起，弹出菜单
    def onRightButtonUp(self,event):
        self.menu.post(event.x_root, event.y_root)
    def Draw_rect(self):
        for rect in self.record_rect:
            self.canvas.create_rectangle(rect[0],rect[1],rect[2],rect[3],  outline=self.foreColor,width=3)
    def Clear(self):
        for item in self.canvas.find_all():
            print('item',item)
            self.canvas.delete(item)
        self.end=[0]
        self.lastDraw=0
        self.update_img(self.img)
        self.record_rect.clear()

    def update_img(self,img):
        if img is not None:
            cv2image = cv2.cvtColor(img, cv2.COLOR_BGR2RGBA)
            current_image = Image.fromarray(cv2image)
            imgtk = ImageTk.PhotoImage(image=current_image)
            self.canvas.create_image(img.shape[1] / 2,img.shape[0] / 2, image = imgtk)
            self.canvas.img = imgtk