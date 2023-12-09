import cv2
import random
import math
import numpy as np
from glob import glob


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

def get_cneter_image(image,scale=0.5,min_area=80000,max_area=200000):
    """
    """
    h, w = image.shape[0], image.shape[1]
    h, w = int(h * scale), int(w * scale)
    image = cv2.resize(image, (w, h))
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    ret, thresh1 = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY)
    contours, hierarchy = cv2.findContours(thresh1, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for c in range(len(contours)):
        area = cv2.contourArea(contours[c])
        if max_area > area > min_area:
            x_, y_, w_, h_ = cv2.boundingRect(contours[c])
            # print(x_, y_, w_, h_)
            a, b = max(w_, h_), min(w_, h_)
            if a / b < 1.5:
                cx,cy = cal_center(contours[c])
                std = distances_zoo(contours[c],cx,cy)
                if std < 5:
                    # cv2.drawContours(image, contours, c, (0, 0, 255), 2, 8)
                    # cv2.rectangle(image, (x_, y_), (x_ + w_, y_ + h_), (0, 255, 0), 2)
                    # cv2.circle(image, (center_x, center_y), 2, (0, 255, 0), 10)  # 画圆心
                    # cv2.circle(image, (cx, cy), 5, (255, 0, 0), -1)
                    # 显示
                    new_image = image[y_+50:y_+h_-50,x_+50:x_+w_-50]
                    laplacian = cv2.Laplacian(new_image, cv2.CV_16S).var()
                    print('laplacian',laplacian,new_image.shape)
                    return new_image

def get_clear(image,part=20):
    """
    给定一张照片，随机选择part部分个区域，进行清晰度计算
    """
    shape = image.shape
    height, width = shape[0], shape[1]
    # print('height,width',height,width)
    core_size = int(1 / part * min(height, width))
    print('core_size', core_size)

    height_value = height - core_size
    width_value = width - core_size

    height_list = [i for i in range(height_value)]
    width_list = [i for i in range(width_value)]
    height_choose = random.sample(height_list, part)
    width_choose = random.sample(width_list, part)
    # print(height_choose,width_choose)
    kk = zip(height_choose, width_choose)
    clearness_ = []
    for i in kk:
        y = i[0]
        x = i[1]
        new_image = image[y:y+core_size,x:x+core_size]
        value = cal_clear((new_image))
        clearness_.append(value)
        # print(value)
        # cv2.imshow('2',new_image)
        # cv2.waitKey(0)
    array_ = np.array(clearness_)
    mean_ = np.mean(array_)
    std_ = np.std(array_)
    print('mean_,std_',mean_,std_)


def cal_clear(image):
    laplacian = cv2.Laplacian(image, cv2.CV_16S).var()
    return laplacian


if __name__ == "__main__":
    root = "D:/Projects/motor/images_saves"
    image_path = root + '/y3/6_*.png'
    images = glob(image_path)
    for i in images:
        try:
            print(i)
            image = cv2.imread(i)
            image = get_cneter_image(image)
            get_clear(image,20)
        except:
            pass