from hsv import HSV
import cv2
import numpy as np
import math
import random
import copy
from gen_xml import xml

import sys
import os

class extract_obj:
    bule_upper = [221,255,255]
    bule_lower = [167,107,124]
    
    def __init__(self,file_name,Obj_Type):
        self.Makexml = xml()
        self.file_name = file_name
        all_folds = os.listdir('targe/'+self.file_name+'/img/')
        self.img_Num = len(all_folds)
        self.Type = Obj_Type
        pass
    
    def GetMask(self,img):
        obj_roi = None
        hsv = HSV()
        mask = hsv.HSV_Mask(self.bule_upper,self.bule_lower,img)


        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))  # define kernel (5,5)

        dilated = cv2.dilate(mask, kernel, 1)  # dilate
        contours, hierarchy = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        cv2.drawContours(mask, contours, -1, (0, 0, 255), 1)
        # 建立白色畫布
        temp = np.ones(img.shape, np.uint8)*255
        img_debug = img.copy()
        # 畫出輪廓：temp是白色畫布，contours是輪廓，-1表示全畫，然后是颜色，厚度

        # 找出面積最大的等高線區域
        line_width = int(img.shape[1]/500)
        
        # c_max = max(contours, key = cv2.contourArea)
        contours_list = []
        for c in contours:
            # cv2.drawContours(img_debug, [c], -1, (0, 0, 255), line_width)
            # area = cv2.contourArea(c)
            contours_list.append(c)
        
        
        rect = cv2.minAreaRect(contours_list[1])
        box = cv2.boxPoints(rect)
        box = np.int0(box)
        # cv2.drawContours(img_debug, [box], 0, (0, 0, 255), line_width)


        x, y, w, h = cv2.boundingRect(box)
        cv2.rectangle(img_debug,(x, y), (x + w, y + h), (0, 255, 0), line_width)


        print('[box]',[box])





        # # cv.drawContours(img_debug, [box], 0, (0, 0, 255), line_width)
        # temp = np.zeros((img.shape[0],img.shape[1],1), np.uint8)

        # cv2.drawContours(temp, [contours_list[1]], 0, 255, line_width)
        # # cv2.imshow('temp',temp)
        # # cv2.waitKey()

        # # # 得四個角點
        # point_list = self.GetPoint(temp)
        # Corner_list = self.Get_corner([box],point_list)

        # point_size = 2
        # point_color = (0, 0, 255) # BGR
        # thickness = 4 # 可以为 0 、4、8
        # cnt = 0
        # # 畫出腳點
        # for point in Corner_list:
        #     # print('p  oint',point)
        #     cv2.circle(img_debug, (point[0],point[1]), point_size, point_color, thickness)
        #     cv2.putText(img_debug, str(cnt + 1), (point[0] - 20, point[1]),
        #     cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
        #     cnt = cnt + 1


        # # mask,dst = self.fetch_roi(img,Corner_list)

        # cv2.imshow('mask',mask)
        # cv2.waitKey()
        mask = 255 - mask
        dst = cv2.bitwise_and(img, img, mask=mask)
        return mask,[x, y, w, h],dst
    
    def fetch_roi(self,img,point):
        src = img.copy()
        mask = np.zeros((img.shape[0], img.shape[1]), dtype = np.uint8)
        x_list = []
        y_list = []
        for pt in point:
            x_list.append(pt[0])
            y_list.append(pt[1])
        x_data = np.array(x_list)
        y_data = np.array(y_list)
        pts = np.vstack((x_data, y_data)).astype(np.int32).T
        cv2.fillPoly(mask, [pts], ( 255), 8, 0)
        dst = cv2.bitwise_and(src, src, mask=mask)
        # cv2.imshow('dst',dst)
        # cv2.waitKey()
        return mask,dst
    
    def GetPoint(self,img):
        Point_list =[]
        # print('shape',img.shape)
        for y in range(img.shape[0]):
            for x in range(img.shape[1]):
                # print('img[x][y]',img[y][x])
                if(img[y][x] == 255):
                    Point_list.append([x,y])
                    # print('(x,y)',(x,y))
        return Point_list
    
    def Get_corner(self,box,point_corner):
        
        corner_list = []
        point_rect = []

        for b in box:
            for i in b:
                # print(i)
                point_rect.append(i)
        # print('point_rect',point_rect)
        for rect in point_rect:
            Min_dis = 10000
            pt = None
            for corner in point_corner:
                dis = self.Caldis(rect,corner)
                if(Min_dis > dis):
                    pt = corner
                    Min_dis = dis
            corner_list.append(pt)

        # print('corner_list',corner_list)
        return corner_list
    
    def Caldis(self,pt1,pt2):
        return math.sqrt((((pt1[1] - pt2[1])**2) + (pt1[0] - pt2[0])**2))

    def exec(self,img_ori,img_crop,Mask_crop):
        img1 = copy.deepcopy(img_ori)
        img2 = copy.deepcopy(img_crop)
        Mask = copy.deepcopy(Mask_crop)

        scale = random.uniform(1.0,2.0)

        # print('img2.shape',img2.shape)
        print('Mask',Mask.shape)
        size = [int(img2.shape[1] / scale) , int(img2.shape[0] / scale)]
        img2 = cv2.resize(img2, (size[0], size[1]), interpolation=cv2.INTER_CUBIC)
        Mask = cv2.resize(Mask, (size[0], size[1]), interpolation=cv2.INTER_CUBIC)


        r1,c1,ch1 = img1.shape
        r2,c2,ch2 = img2.shape

        # print('img2.shape',img2.shape)
        # print('Mask',Mask.shape)


        offset_range_x = [0,c1 - c2]
        offset_range_y = [0,r1 - r2]

        offset_x = random.randint(offset_range_x[0],offset_range_x[1])
        offset_y = random.randint(offset_range_y[0],offset_range_y[1])

        x_range = [c1 - c2 - offset_x, c1 - offset_x]
        y_range = [r1 - r2 - offset_y, r1 - offset_y]
        
        # 取出右下角
        roi = img1[y_range[0] :y_range[1], x_range[0] :x_range[1]] 

        mask_tmep = Mask
        Mask = 255 - Mask

        fg1 = cv2.bitwise_and(roi,roi,mask=Mask)
        fg2 = cv2.bitwise_and(img2,img2,mask=mask_tmep)
        
        roi[:] = cv2.add(fg1, fg2)
        # bounding box
        bounding = [x_range[0],y_range[0],x_range[1],y_range[1]]
        # print('bounding',bounding)
        # cv2.rectangle(img1, (bounding[0],bounding[1]), (bounding[2], bounding[3]), (0, 255, 0), 2)
        # pic = cv2.resize(img1, (640, 360), interpolation=cv2.INTER_CUBIC)
        

        pic_name = str(self.Type) + '_' + str(self.img_Num) 
        self.Makexml.makexml(   targe_file = self.file_name,
                                Name = pic_name,
                                Type = self.Type,
                                Image = img1,
                                rect = bounding)
        self.img_Num = self.img_Num + 1
        return img1
