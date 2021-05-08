import urllib.request
import cv2
import numpy as np
from pyzbar import pyzbar
from qrReader import getQRS

# cap = cv2.VideoCapture('http://192.168.100.41:8080')
url = "http://192.168.100.41:8080/shot.jpg"

while True:
    imgResp = urllib.request.urlopen(url)
    imgNp = np.array(bytearray(imgResp.read()), dtype=np.uint8)
    img = cv2.imdecode(imgNp, -1)
    qr = getQRS(img)
    print(qr)
    cv2.imshow('test', img)
    if ord('q') == cv2.waitKey(10):
        exit(0)