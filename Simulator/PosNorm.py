from os import sys
sys.path.append('C:/Users/PedroLuis/Clases-Robotica/Lib')

import urllib.request
import cv2
import numpy as np
from pyzbar import pyzbar
from pyzbar.pyzbar import decode
from qrReader import getQRS


def getPosNorm(img):
    result = []
    W = img.shape[1] #ancho imagen
    H = img.shape[0] #alto imagen

    for QR in decode(img):
        #print(QR.data)
        myData = QR.data.decode('utf-8')
        #print(myData)
        pts = np.array([QR.polygon], np.int32)
        pts = pts.reshape((-1, 1, 2))
        pts2 = QR.rect
        cv2.polylines(img, [pts], True, (255,0,0),5)
        cv2.putText(img, myData, (pts2[0], pts2[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.9, [255,0,255], 2)

        wc = pts2.width # ancho QR
        hc = pts2.height # alto QR

        # centroide QR
        Cx = ((pts[0][0][0]+pts[2][0][0]))/2
        Cy = ((pts[0][0][1]+pts[2][0][1]))/2

        [xn,yn]=[Cx/W,Cy/H] # posicion normalizada
        [wn,hn]=[wc/W,hc/H] # tamaño normalizado
        result.append({"x":xn,"y":yn,"w":wn,"h":hn})
    return result

def centroMasa(img):
    #convertir a HSV
    imageHSV=cv2.cvtColor(img,cv2.COLOR_BGR2HSV)

    #filtrado
    minH=np.array([0,0,0])
    maxH=np.array([14,255,255])
    binaryImage=cv2.inRange(imageHSV,minH,maxH)

    cv2.imwrite("binary.png",binaryImage)
    cv2.imwrite("camera.png",img)

    #calcular los momentos
    #Segundo argumento normaliza en caso de que sea binario 
    moments=cv2.moments(binaryImage,True)

    #El area de la imagen 
    areaObject=moments['m00']

    #area Image
    areaImage=binaryImage.shape[0]*binaryImage.shape[1]

    #posicion centro de masa
    xcenter=moments['m10']/moments['m00']
    ycenter=moments['m01']/moments['m00']    
    return areaObject, areaImage, xcenter, ycenter, binaryImage

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

def contour_img(img):
    img_grey = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    #set a thresh
    thresh = 100
    #get threshold image
    ret,thresh_img = cv2.threshold(img_grey, thresh, 255, cv2.THRESH_BINARY)
    #find contours
    contours, hierarchy = cv2.findContours(thresh_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    #create acopy of the image for contours
    img_contours = img.copy()

    # draw the contours on the empty image
    cv2.drawContours(img_contours, contours, -1, (0,255,0), 3)

    return img_contours

#main
if __name__ == "__main__":
    # cap = cv2.VideoCapture('http://192.168.100.41:8080')
    url = "http://192.168.100.41:8080/shot.jpg"

    while True:
        imgResp = urllib.request.urlopen(url)
        imgNp = np.array(bytearray(imgResp.read()), dtype=np.uint8)
        img = cv2.imdecode(imgNp, -1)

    # Hallando el centro de masa del recuadro por Momentos
        areaObject, areaImage, xcenter, ycenter, binaryImage = centroMasa(img)
        print("Recuadro (Utilizando Momentos)\nArea",areaObject/areaImage)
        print("CM X", xcenter/binaryImage.shape[1], "\nCM Y", ycenter/binaryImage.shape[0])
        
    #posicion
        print(getPosNorm(img))
        print("\n")
    
    #Contorno
        #img = contour_img(img) #Todavia no marca bien el marco

    #Imagen con QR resaltado
        resized = resize_img(img)
        cv2.imshow('Resultado',resized)

        if ord('q') == cv2.waitKey(10):
            exit(0)