from os import sys
sys.path.append('C:/Users/PedroLuis/Clases-Robotica/Lib')

import urllib.request
import cv2
import numpy as np
from pyzbar import pyzbar
from pyzbar.pyzbar import decode
from qrReader import getQRS


def resize_img(img):
    # Image Scaling
    scale_percent = 50
    width = int(img.shape[1] * scale_percent / 100)
    height = int(img.shape[0] * scale_percent / 100)
    # dsize
    dsize = (width, height)
    # resize image
    resized = cv2.resize(img, dsize)
    return resized


if __name__ == "__main__":
    url = "http://192.168.100.41:8080/shot.jpg"

    while True:
        imgResp = urllib.request.urlopen(url)
        imgNp = np.array(bytearray(imgResp.read()), dtype=np.uint8)
        img = cv2.imdecode(imgNp, -1)
        img = resize_img(img)
        imageGRAY=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        img = cv2.Canny(img, 100, 200)
        cv2.imshow("hola",img)
        contours = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        img = cv2.drawContours(img, contours,1,1 )

        if ord('q') == cv2.waitKey(10):
            exit(0)
