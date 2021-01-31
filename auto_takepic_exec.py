# -*- coding: utf-8 -*
import cv2
Img = None
img_Num = -1
angle = 0.0
def init_cam(self,cam_idx):
    cam1 = cv2.VideoCapture(cam_idx) 

    cam1.set(cv2.CAP_PROP_FRAME_WIDTH, 640)  # 寬
    cam1.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)  # 高

    return cam1

def photo_callback(self,e, x, y, f, p):
    global Img,img_Num
    if e == cv2.EVENT_LBUTTONDOWN:
        saveImg(Img,img_Num)

def saveImg(Img,img_Num):
    global angle
    if(angle < 360):
        cv2.imwrite('img/'+ sys.argv[1] + '/' + str(img_Num) +'.bmp',Img)
        img_Num = img_Num + 1
        '''
        動馬達程式
        '''
        angle = angle + 1.5

if __name__ == "__main__":
    global Img,img_Num
    counter = 0
    all_folds = os.listdir('img/'+sys.argv[1])
    img_Num = len(all_folds)

    camera = init_cam(2)
    cv2.namedWindow("Camera")
    cv2.setMouseCallback("Camera", photo_callback, None)
    while (cv2.waitKey(1)!= 27):
        ret1, Img = camera.read()
        if(ret1 == True):
            cv2.imshow('Camera',Img)
            counter = counter + 1
            if(counter > 2 * 1000):
                saveImg(Img,img_Num)
                counter = 0
