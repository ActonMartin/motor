import cv2
from glob import glob
import numpy as np
import matplotlib.pyplot as plt
import math


def cal_center(contour):
    """
    type(contour) numpy
    """
    # calculate moments of binary image
    M = cv2.moments(contour)

    # calculate x,y coordinate of center
    cX = int(M["m10"] / M["m00"])
    cY = int(M["m01"] / M["m00"])
    return cX,cY


def distances_zoo(contour,cx,cy):
    """
    type(contour) numpy
    """
    distances_ = []
    for i in range(len(contour)):
        contour_a = np.squeeze(contour[i])
        distance = math.sqrt(math.pow(contour_a[0]-cx,2)+math.pow(contour_a[1]-cy,2))
        distances_.append(distance)
    # mean_distances = np.mean(distances_)
    std_distance = np.std(distances_)
    return std_distance

def test_one(root):
    image_path = root + '/y5/2_0_1.png'
    image = cv2.imread(image_path)
    h,w = image.shape[0],image.shape[1]
    h,w = int(h*0.5),int(w*0.5)
    image = cv2.resize(image,(w,h))
    GrayImage = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    ret, thresh1 = cv2.threshold(GrayImage, 127, 255, cv2.THRESH_BINARY)
    ret, thresh2 = cv2.threshold(GrayImage, 127, 255, cv2.THRESH_BINARY_INV)
    ret, thresh3 = cv2.threshold(GrayImage, 127, 255, cv2.THRESH_TRUNC)
    ret, thresh4 = cv2.threshold(GrayImage, 127, 255, cv2.THRESH_TOZERO)
    ret, thresh5 = cv2.threshold(GrayImage, 127, 255, cv2.THRESH_TOZERO_INV)
    titles = ['Gray Image', 'BINARY', 'BINARY_INV', 'TRUNC', 'TOZERO', 'TOZERO_INV']
    images = [GrayImage, thresh1, thresh2, thresh3, thresh4, thresh5]
    for i in range(6):
        plt.subplot(2, 3, i + 1), plt.imshow(images[i], 'gray')
        plt.title(titles[i])
        plt.xticks([]), plt.yticks([])
    plt.show()
    # cv2.imshow('2',GrayImage)
    # cv2.waitKey(0)

def test2(image_path):
    image = cv2.imread(image_path)
    h, w = image.shape[0], image.shape[1]
    h, w = int(h * 0.5), int(w * 0.5)
    image = cv2.resize(image, (w, h))
    GrayImage = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    ret, thresh1 = cv2.threshold(GrayImage, 127, 255, cv2.THRESH_BINARY)
    # kernel = np.ones((5, 5), np.uint8)  # 创建全一矩阵，数值类型设置为uint8
    # erosion = cv2.erode(thresh1, kernel, iterations=1)  # 腐蚀处理
    # dilation = cv2.dilate(erosion, kernel, iterations=1)  # 膨胀处理

    # imgray = cv2.Canny(thresh1, 80, 100)  # Canny算子边缘检测

    circles = cv2.HoughCircles(thresh1,cv2.HOUGH_GRADIENT,1,80,param1=100,param2=20,minRadius=150,maxRadius=300)#霍夫圆变换
    if circles is not None:
        circles = circles.reshape(-1, 3)
        # circles = np.uint16(np.around(circles))

        for i in circles:
            print(i[2])
            cv2.circle(image, (i[0], i[1]), i[2], (0, 0, 255), 5)  # 画圆
            cv2.circle(image, (i[0], i[1]), 2, (0, 255, 0), 10)  # 画圆心
        cv2.imshow('2', image)
        cv2.waitKey(0)
    else:
        cv2.imshow('2', image)
        cv2.waitKey(0)
        print(image_path+"没有找到圆")

def test3(image_path):
    image = cv2.imread(image_path)
    # print(image.shape)
    h, w = image.shape[0], image.shape[1]
    h, w = int(h * 0.5), int(w * 0.5)
    image = cv2.resize(image, (w, h))
    GrayImage = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    ret, thresh1 = cv2.threshold(GrayImage, 127, 255, cv2.THRESH_BINARY)
    contours, hierarchy = cv2.findContours(thresh1, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # print('contours长度',len(contours))
    for c in range(len(contours)):
        area = cv2.contourArea(contours[c])
        # print(area)
        if 300000 > area > 80000:
            x_, y_, w_, h_ = cv2.boundingRect(contours[c])
            a,b = max(w_,h_),min(w_,h_)
            if a/b <1.5:
                # print(x_, y_, w_, h_)
                # center_x = x_ + int(0.5*w_)
                # center_y = y_ + int(0.5*h_)
                cx,cy = cal_center(contours[c])
                std = distances_zoo(contours[c],cx,cy)
                if std < 5:
                    # cv2.drawContours(image, contours, c, (0, 0, 255), 2, 8)
                    # cv2.rectangle(image, (x_, y_), (x_ + w_, y_ + h_), (0, 255, 0), 2)
                    # cv2.circle(image, (center_x, center_y), 2, (0, 255, 0), 10)  # 画圆心
                    # cv2.circle(image, (cx, cy), 5, (255, 0, 0), -1) #画形心
                    # 显示
                    new_image = image[y_+50:y_+h_-50,x_+50:x_+w_-50]
                    laplacian = cv2.Laplacian(new_image,cv2.CV_16S).var()
                    # cv2.imshow("2", image)
                    # cv2.waitKey(0)
                    # print(laplacian,image_path)
                    return laplacian,image_path,new_image
                # cv2.drawContours(image, contours, c, (0, 0, 255), 2, 8)
                # cv2.rectangle(image, (x_, y_), (x_ + w_, y_ + h_), (0, 255, 0), 2)
                # new_image = image[y_ + 110:y_ + h_ - 110, x_ + 110:x_ + w_ - 110]
                # laplacian = cv2.Laplacian(new_image, cv2.CV_16S).var()
                # cv2.imshow("2", image)
                # cv2.waitKey(0)
                # # print(laplacian,image_path)
                # return laplacian, image_path

def canny_demo(image):
    t = 80
    canny_output = cv2.Canny(image, t, t * 2)
    # cv2.imshow("canny_output", canny_output)
    cv2.imwrite("D:/Projects/motor/images_saves/canny_output.png", canny_output)
    return canny_output

if __name__ == '__main__':

    root = "D:/Projects/motor/images_saves"
    image_path = root + '/y3/24_*.png'
    images = glob(image_path)
    # print(images)
    val_ = []
    path_ = []
    images_ = []
    for i in images:
        # print(i)
        # test3(i)
        try:
            value,path,image = test3(i)
            val_.append(value)
            path_.append(path)
            images_.append(image)
        except:
            pass
    # print('val_',val_)
    print('max(val_)',max(val_))
    a_maxindex = np.where(val_==max(val_))[0][0] # 最大索引
    print(path_[a_maxindex])
    # cv2.imshow('33',images_[a_maxindex])
    # cv2.waitKey(0)
    target_image = images_[a_maxindex]
    cv2.imwrite('D:/Projects/motor/images_saves/99855.png',target_image)

    binary = canny_demo(target_image)
    k = np.ones((5, 5), dtype=np.uint8)
    binary = cv2.morphologyEx(binary, cv2.MORPH_DILATE, k)

    gray_image = cv2.cvtColor(target_image,cv2.COLOR_BGR2GRAY)
    kernel = np.ones((9,9))
    gray_image = cv2.dilate(gray_image,kernel)

    ret, thresh1 = cv2.threshold(gray_image, 200, 255, cv2.THRESH_BINARY)
    ret, thresh2 = cv2.threshold(gray_image, 200, 255, cv2.THRESH_BINARY_INV)
    ret, thresh3 = cv2.threshold(gray_image, 200, 255, cv2.THRESH_TRUNC)
    ret, thresh4 = cv2.threshold(gray_image, 200, 255, cv2.THRESH_TOZERO)
    ret, thresh5 = cv2.threshold(gray_image, 200, 255, cv2.THRESH_TOZERO_INV)
    titles = ['Gray Image', 'BINARY', 'BINARY_INV', 'TRUNC', 'TOZERO', 'TOZERO_INV']
    images = [gray_image, binary, thresh2, thresh3, thresh4, thresh5]
    for i in range(6):
        plt.subplot(2, 3, i + 1), plt.imshow(images[i], 'gray')
        plt.title(titles[i])
        plt.xticks([]), plt.yticks([])
    plt.show()



    # contours, hierarchy = cv2.findContours(thresh1, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE) # 通过thresh1进行轮廓寻找
    contours, hierarchy = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) # 通过binary进行轮廓寻找
    count = 0
    for c in range(len(contours)):
        x, y, w, h = cv2.boundingRect(contours[c])
        min_,max_ = min(w,h),max(w,h)
        if max_/min_ < 3:
            area = cv2.contourArea(contours[c])
            if area < 500:
                count += 1
                print('面积',area)
                cv2.drawContours(target_image, contours, c, (0, 0, 255), 2, 8)
    print('count',count)
    # for c in range(len(contours)):
    #     if len(contours[c]) >= 5:
    #         area = cv2.contourArea(contours[c])
    #         if area < 500:
    #             print(area)
    #             # 椭圆拟合
    #             (cx, cy), (a, b), angle = cv2.fitEllipse(contours[c])
    #             # 绘制椭圆
    #             cv2.ellipse(target_image, (np.int32(cx), np.int32(cy)),
    #                    (np.int32(a / 2), np.int32(b / 2)), angle, 0, 360, (0, 0, 255), 2, 8, 0)
    cv2.imshow('33',target_image)
    cv2.waitKey(0)