import cv2
import numpy as np 

cv2.namedWindow("original")
cv2.namedWindow("filtered")

def callback(x):
    pass

cv2.createTrackbar("minH","original",0,255,callback)
cv2.createTrackbar("maxH","original",255,255,callback)

# video capture args 
# Si es un numerico 0,1,2
# Si es una url lee el buffer de video
cam=cv2.VideoCapture(0)

while(cam.isOpened()):
    frame=cv2.imread("../Moments/huImages/original.jpg")
    cv2.imshow("original",frame)

    #obtener imagen en HSV
    imageHSV=cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)

    #getTrackbarpos obtiene el valor actual del slider 
    minH=cv2.getTrackbarPos("minH","original")
    maxH=cv2.getTrackbarPos("maxH","original")

    #Definicion del rango
    #120,20,20 minH=140 maxH=200
    minHSV=np.array([minH,0,0])
    maxHSV=np.array([maxH,255,255])

    #inrange convierte a 255 todos los pixeles en el rango de minHSV y maxHSV, y el resto los deja en 0
    mask=cv2.inRange(imageHSV,minHSV,maxHSV)
    cv2.imshow("filtered",mask)
    cv2.imshow("original",frame)


    #waitkey devuelve el asci de la tecla oprimida
    key=cv2.waitKey(1)
    if(key==ord("q")):
        break

cv2.destroyAllWindows();




