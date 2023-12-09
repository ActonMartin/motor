import cv2
import numpy as np
import math


def process_neiwu(image,scale=0.5,min_area=80000,max_area=200000):
    h, w = image.shape[0], image.shape[1]
    h, w = int(h * scale), int(w * scale)
    image = cv2.resize(image, (w, h))
    # GrayImage = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    ret, thresh1 = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY)
    contours, hierarchy = cv2.findContours(thresh1, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for c in range(len(contours)):
        area = cv2.contourArea(contours[c])
        if max_area > area > min_area:
            x_, y_, w_, h_ = cv2.boundingRect(contours[c])
            print(x_, y_, w_, h_)
            a, b = max(w_, h_), min(w_, h_)
            if a / b < 1.5:
                # cv2.drawContours(image, contours, c, (0, 0, 255), 2, 8)
                # cv2.rectangle(image, (x_, y_), (x_ + w_, y_ + h_), (0, 255, 0), 2)
                new_image = image[y_:y_ + h_, x_:x_ + w_]
                return new_image

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


def process_neiwu_all(image_array_list,scale=0.5,min_area=80000,max_area=200000):
    """
    输入一组拍摄的照片，返回内污清晰的那一张照片
    """
    # print(image.shape)
    laplacian_list = []
    new_images_list = []
    last = []
    for image in image_array_list:
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
                        laplacian = cv2.Laplacian(new_image,cv2.CV_16S).var()
                        # print(laplacian)
                        # cv2.imshow("2", image)
                        # cv2.waitKey(0)
                        laplacian_list.append(laplacian)
                        new_images_list.append(new_image)

    if laplacian_list:
        print('laplacian_list',laplacian_list)
        print('len(laplacian_list)',len(laplacian_list))
        print('len(new_images_list)',len(new_images_list))
        index_ = np.where(laplacian_list == max(laplacian_list))[0][0]
        print('index_',index_)
        # kk = new_images_list[index_]
        # cv2.imshow('kk',kk)
        # cv2.waitKey(0)
        last.append(new_images_list[index_])
        return last
    else:
        last.append(np.zeros((800, 800, 1), dtype='uint8'))
        return last

if __name__ == "__main__":
    from glob import glob
    root = "D:/Projects/motor/images_saves"
    image_path = root + '/y4/1_*.png'
    images = glob(image_path)
    # print(images)
    images_list = []
    for i in images:
        image = cv2.imread(i)
        images_list.append(image)
    oo = process_neiwu_all(images_list)
    # print(type(oo),len(oo))
    cv2.imshow('2',oo[0])
    cv2.waitKey(0)