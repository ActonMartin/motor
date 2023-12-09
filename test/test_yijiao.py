import cv2
from glob import glob
import os
import matplotlib.pyplot as plt
import warnings
import numpy as np


def test_one(image_path):
    warnings.warn('代码不使用了，已经废除',DeprecationWarning)
    image = cv2.imread(image_path)
    h,w = image.shape[0],image.shape[1]
    h,w = int(h*0.5),int(w*0.5)
    image = cv2.resize(image,(w,h))
    GrayImage = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    ret, thresh1 = cv2.threshold(GrayImage, 127, 255, cv2.THRESH_BINARY)
    ret, thresh2 = cv2.threshold(GrayImage, 127, 255, cv2.THRESH_BINARY_INV)
    ret, thresh3 = cv2.threshold(GrayImage, 127, 255, cv2.THRESH_TRUNC)
    ret, thresh4 = cv2.threshold(GrayImage, 127, 255, cv2.THRESH_TOZERO)
    ret, thresh5 = cv2.threshold(GrayImage, 127, 255, cv2.THRESH_TOZERO_INV)
    titles = ['HSV Image', 'BINARY', 'BINARY_INV', 'TRUNC', 'TOZERO', 'TOZERO_INV']
    images = [GrayImage, thresh1, thresh2, thresh3, thresh4, thresh5]
    for i in range(6):
        plt.subplot(2, 3, i + 1), plt.imshow(images[i], 'gray')
        plt.title(titles[i])
        plt.xticks([]), plt.yticks([])
    plt.show()


def find_zui_liang(image_path):
    warnings.warn('代码不使用了，已经废除', DeprecationWarning)
    image = cv2.imread(image_path)
    h, w = image.shape[0], image.shape[1]
    h, w = int(h * 0.5), int(w * 0.5)
    image = cv2.resize(image, (w, h))
    GrayImage = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # 利用cv2.minMaxLoc寻找到图像中最亮和最暗的点
    (minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(GrayImage)
    # 在图像中绘制结果
    cv2.circle(image, maxLoc, 5, (255, 0, 0), 2)
    cv2.imshow('2',image)
    cv2.waitKey(0)


def find__(image_path):
    warnings.warn('代码不使用了，已经废除', DeprecationWarning)
    img = cv2.imread(image_path,0)
    # global thresholding
    ret1, th1 = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)
    # Otsu's thresholding
    ret2, th2 = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    # Otsu's thresholding after Gaussian filtering
    blur = cv2.GaussianBlur(img, (5, 5), 0)
    ret3, th3 = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    # plot all the images and their histograms
    images = [img, 0, th1,
              img, 0, th2,
              blur, 0, th3]
    titles = ['Original Noisy Image', 'Histogram', 'Global Thresholding (v=127)',
              'Original Noisy Image', 'Histogram', "Otsu's Thresholding",
              'Gaussian filtered Image', 'Histogram', "Otsu's Thresholding"]
    for i in range(3):
        plt.subplot(3, 3, i * 3 + 1), plt.imshow(images[i * 3], 'gray')
        plt.title(titles[i * 3]), plt.xticks([]), plt.yticks([])
        plt.subplot(3, 3, i * 3 + 2), plt.hist(images[i * 3].ravel(), 256)
        plt.title(titles[i * 3 + 1]), plt.xticks([]), plt.yticks([])
        plt.subplot(3, 3, i * 3 + 3), plt.imshow(images[i * 3 + 2], 'gray')
        plt.title(titles[i * 3 + 2]), plt.xticks([]), plt.yticks([])
    plt.show()


def find_histogram(image_path):
    warnings.warn('代码不使用了，已经废除', DeprecationWarning)
    import cv2
    import numpy as np
    import matplotlib.pyplot as plt
    # 加载图片
    img = cv2.imread(image_path)
    # 把图片的BGR色彩空间转换成RGB色彩空间
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    # 显示图片
    # plt.imshow(img)
    # 使用 np.histogram 函数计算直方图
    hist, bins = np.histogram(img, 256, [0, 255])
    # 使用 plt.fill 函数 填充多边形
    plt.fill(hist)
    #  标记x轴的名称
    plt.xlabel('pixel value')
    # 显示直方图
    plt.show()


def find_adaptiveThreshold(image_path):
    warnings.warn('代码不使用了，已经废除', DeprecationWarning)
    # -*- coding: utf-8 -*-
    import cv2
    import numpy as np
    from matplotlib import pyplot as plt

    img = cv2.imread(image_path, 0)  # 0是第二个参数，将其转为灰度图

    img = cv2.medianBlur(img, 5)
    ret, th1 = cv2.threshold(img, 240, 255, cv2.THRESH_BINARY)

    # 11 为 邻域大小,   2为C值，常数
    th2 = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_MEAN_C, \
                                cv2.THRESH_BINARY, 51, 2)
    th3 = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, \
                                cv2.THRESH_BINARY, 51, 2)

    titles = ['Original Image', 'Global Thresholding (v = 240)',
              'Adaptive Mean Thresholding', 'Adaptive Gaussian Thresholding']
    images = [img, th1, th2, th3]
    for i in range(4):
        plt.subplot(2, 2, i + 1), plt.imshow(images[i], 'gray')
        plt.title(titles[i])
        plt.xticks([]), plt.yticks([])
    plt.show()

def find_yijiao(image_path):
    # print(image_path)
    image = cv2.imread(image_path)
    image_gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    image_blur = cv2.medianBlur(image_gray, 5)
    ret, thresh1 = cv2.threshold(image_blur, 240, 255, cv2.THRESH_BINARY)

    kernel = np.ones((5, 5), np.uint8)
    dilate = cv2.dilate(thresh1,kernel)
    # thresh1_ = cv2.cvtColor(dilate, cv2.COLOR_GRAY2RGB)
    crc = cv2.HoughCircles(dilate, cv2.HOUGH_GRADIENT, 2, 1500, param1=100, param2=10, minRadius=600, maxRadius=900)

    k_image_ = np.zeros_like(image)
    # k_image = cv2.cvtColor(k_image_,cv2.COLOR_BGR2GRAY)
    # print(k_image.shape)
    if crc is not None:
        # Convert the coordinates and radius of the circles to integers
        crc = np.round(crc[0, :]).astype("int")
        # For each (x, y) coordinates and radius of the circles
        for (x, y, r) in crc:
            # Draw the circle -1为内部填充为白色
            cv2.circle(k_image_, (x, y), r, (255, 255, 255), -1)
            # Print coordinates
            # print("x:{}, y:{}".format(x, y))

    # titles = ['Original Image', 'Global Thresholding (v = 240)']
    # images = [image, thresh1_]
    # for i in range(2):
    #     plt.subplot(1, 2, i + 1), plt.imshow(images[i])
    #     plt.title(titles[i])
    #     plt.xticks([]), plt.yticks([])
    # plt.show()

    mask = k_image_



    last = cv2.bitwise_and(image,mask)
    # print(last.shape)
    end = np.hstack([image,last])
    end = cv2.resize(end,(0,0),fx=0.5,fy=0.5)
    cv2.imshow("out", end)

    # cv2.imshow('2',k_image_)
    cv2.waitKey(0)

    # return thresh1


if __name__ == "__main__":
    root = "D:/Projects/motor/test/yijiao"
    path_sniffer = root + '/*.jpg'
    images_path = glob(path_sniffer, recursive=True)
    count = 0
    for i in images_path:
        print(i)
        find_yijiao(i)
        count += 1
        if count == 20:
            break
        # test_one(i)
        # find_zui_liang(i)
        # find__(i)
        # find_histogram(i)
        # find_adaptiveThreshold(i)
        # break
