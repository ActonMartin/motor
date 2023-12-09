import cv2
import numpy as np
from glob import glob


def process_yijiao(image):
    # image = cv2.imread(image_path)
    image_gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    image_blur = cv2.medianBlur(image_gray, 5)
    ret, thresh1 = cv2.threshold(image_blur, 240, 255, cv2.THRESH_BINARY)
    kernel = np.ones((5, 5), np.uint8)
    dilate = cv2.dilate(thresh1,kernel)
    crc = cv2.HoughCircles(dilate, cv2.HOUGH_GRADIENT, 2, 1500, param1=100, param2=10, minRadius=600, maxRadius=900)
    k_image_ = np.zeros_like(image)
    if crc is not None:
        # Convert the coordinates and radius of the circles to integers
        crc = np.round(crc[0, :]).astype("int")
        # For each (x, y) coordinates and radius of the circles
        for (x, y, r) in crc:
            # Draw the circle -1为内部全部填充、并且填充颜色为白色
            cv2.circle(k_image_, (x, y), r, (255, 255, 255), -1)
    mask = k_image_
    last = cv2.bitwise_and(image,mask)
    return last


if __name__ == "__main__":
    root = "D:/Projects/motor/test/yijiao"
    path_sniffer = root + '/*.jpg'
    images_path = glob(path_sniffer, recursive=True)
    count = 0
    for i in images_path:
        print(i)
        image = cv2.imread(i)
        process_yijiao(image)
        count += 1
        if count == 20:
            break