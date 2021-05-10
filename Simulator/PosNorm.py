import urllib.request
import cv2
import numpy as np
from pyzbar import pyzbar
# from lib.qrReader import getQRS

def getQRS(img):
    return [{
        'polygon': QR.polygon,
        'rect': QR.rect,
        'text': QR.data.decode('utf-8')
    }
        for QR in pyzbar.decode(img)]

def getPosNorm(img):
    result = []
    W = img.shape[1] #ancho imagen
    H = img.shape[0] #alto imagen

    for QR in getQRS(img):
        print(QR)
        wc = QR['rect'].width #ancho QR
        hc = QR['rect'].height #alto QR
        Cx, Cy = 0, 0 # se inicializan coordenadas del centroide en 0
        for point in QR['polygon']: # se recorren los puntos del poligono del QR
            Cx += point.x
            Cy += point.y
        Cx/=4; Cy/=4 # se obtiene el centroide
        [xn,yn]=[Cx/W,Cy/H] # posicion normalizada del QR
        [wn,hn]=[wc/W,hc/H] # tamaño normalizado de la imagen
        result.append({"x":xn,"y":yn,"w":wn,"h":hn})
    return result


#main

# cap = cv2.VideoCapture('http://192.168.100.41:8080')
url = "http://192.168.100.41:8080/shot.jpg"

while True:
    imgResp = urllib.request.urlopen(url)
    imgNp = np.array(bytearray(imgResp.read()), dtype=np.uint8)
    img = cv2.imdecode(imgNp, -1)
    
# Image Scaling
    scale_percent = 50
    width = int(img.shape[1] * scale_percent / 100)
    height = int(img.shape[0] * scale_percent / 100)
    # dsize
    dsize = (width, height)
    # resize image
    resized = cv2.resize(img, dsize)

    print(getQRS(img))
    cv2.imshow('test', resized)


# Hallando el centro de masa del recuadro

    #convertir a HSV
    imageHSV=cv2.cvtColor(resized,cv2.COLOR_BGR2HSV)

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

    print("Area",areaObject/areaImage)
    print(xcenter/binaryImage.shape[1],ycenter/binaryImage.shape[0])

#posicion
    print(getPosNorm(img))
    print("\n")
    if ord('q') == cv2.waitKey(10):
        exit(0)