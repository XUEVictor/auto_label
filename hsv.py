import cv2 as cv
import numpy as np
import copy
class HSV:

    green_lower = [50,115,0]
    green_upper = [188,255,255]

    def __init__(self):
        pass
    def HSV_Mask(self,upper, lower, img_ori):
        img = copy.deepcopy(img_ori)
        # 讀圖時是8,擴大到32
        im_bgr = np.float32(img)
        # 擴大後需要正規劃
        im_bgr = im_bgr * (1.0/255.0)
        hsv = cv.cvtColor(im_bgr, cv.COLOR_BGR2HSV)

        hmin = lower[0]
        smin = lower[1]
        vmin = lower[2]

        hmax = upper[0]
        smax = upper[1]
        vmax = upper[2]

        smin_Max = 255
        smax_Max = 255
        vmin_Max = 255
        vmax_Max = 255

        lower_b = np.array([hmin, smin / float(smin_Max), vmin / float(vmin_Max)])
        upper_b = np.array([hmax, smax / float(smax_Max), vmax / float(vmax_Max)])

        mask = cv.inRange(hsv, lower_b, upper_b)

        return mask

    def Background_split(self,img,upper,lower):
        # print('upper',upper)
        # print('lower',lower)

        kernel = cv.getStructuringElement(cv.MORPH_RECT, (3, 3))  # define kernel (5,5)
        green_mask = self.HSV_Mask(upper,lower,img)
        # temp = np.ones(img.shape, np.uint8)*255
        # eroded = cv.erode(green_mask, kernel, 1)  # erode
        # dilated = cv.dilate(eroded, kernel, 3)  # dilate
        # 高斯濾波
        # blur = cv.GaussianBlur(dilated, (3, 3), 0)

        contours, hierarchy = cv.findContours(green_mask, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
        cv.drawContours(green_mask, contours, -1, (0, 0, 255), 1)
        # cv.imshow('green_mask',green_mask)
        # 建立白色畫布
        temp = np.ones(img.shape, np.uint8)*255
        img_debug = img.copy()
        # 畫出輪廓：temp是白色畫布，contours是輪廓，-1表示全畫，然后是颜色，厚度

        # 找出面積最大的等高線區域
        line_width = int(img.shape[1]/500)
        c_max = max(contours, key = cv.contourArea)
        
        # x, y, w, h = cv.boundingRect(c_max)
        # cv.rectangle(img_debug,(x, y), (x + w, y + h), (0, 255, 0), line_width)
        
        rect = cv.minAreaRect(c_max)
        box = cv.boxPoints(rect)
        box = np.int0(box)

        cv.drawContours(img_debug, [box], 0, (0, 0, 255), line_width)
        # cv.imshow('img_debug',img_debug)
        # cv.waitKey(0)
        return box

    def RerangePoint(self,img,box):
        assort_direcion = np.array([[-50,-50],[-50,50],[50,50],[50,-50]])
        img_cx = img.shape[1] / 2
        img_cy = img.shape[0] / 2

        data = box[0]
        '''
        ----------------------隨便亂寫的-------------------------------
        '''
        x_max = 0
        y_max = 0
        for i in box:
            x_error = abs(i[0] - data[0])
            y_error = abs(i[0] - data[0])


            if(x_max < x_error):
                x_max = x_error
            if(y_max < y_error):
                y_max = y_error
        

        left_up = [1280,1280]


        for i in box:
           if(i[0] < left_up[0] and i[1] < left_up[1]):
               left_up = i

        img_cx = left_up[0] + (x_max/2.0)
        img_cy = left_up[1] + (y_max/2.0)

        src = []
        '''
        ----------------------隨便亂寫的-------------------------------
        '''

        # print('len(box)',len(box))
        for j in range(4):
            Max = 0
            Max_idx = -1
            for i in range(len(box)):
                ans = (box[i][0] - img_cx) * assort_direcion[j][0] + (box[i][1] - img_cy) * assort_direcion[j][1]
                if(ans>Max):
                    Max = ans
                    Max_idx = i

            # print('box[Max_idx] : ',box[Max_idx])
            src.append(box[Max_idx])
        return src

    def box2rect(self,img,box):
        Rerange_box = self.RerangePoint(img,box)
        dis = Rerange_box[2] -  Rerange_box[0]
        print('Rerange_box ',Rerange_box)
        return [Rerange_box[0][0],Rerange_box[0][1],dis[0],dis[1]]

    def offsetROI(self,offset,roi):
        for pt in roi:
            pt[0] = pt[0] + offset[0]
            pt[1] = pt[1] + offset[1]
        return roi


    def find_roi(self,img,rect):
        x = rect[0]
        y = rect[1]
        w = rect[2] - rect[0]
        h = rect[3] - rect[1]

        roi = img[y:y+h, x:x+w]

        box = self.Background_split(roi,self.green_upper,self.green_lower)
        box_ = self.box2rect(img,box)
        box_[0] = box_[0] + x
        box_[1] = box_[1] + y
        Image = self.crop(img,box_)
        cv.imshow('Image',Image)
        cv.waitKey()
        return [box_[0],box_[1],box_[0] + box_[2],box_[1] + box_[3]] 

    def crop(self,img,roi):
        (x, y) = (roi[0], roi[1])
        (w, h) = (roi[2], roi[3])
        return img[y:y+h, x:x+w]