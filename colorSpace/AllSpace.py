import cv2 
import numpy as np

image=cv2.imread("./test.jpg")

#resize de la imagen 
image=cv2.resize(image,(700,700))

#convertir a HSV
imageHSV=cv2.cvtColor(image,cv2.COLOR_BGR2HSV)


#convertir a Lab 
imageLab=cv2.cvtColor(image,cv2.COLOR_BGR2LAB)


#mostrar las imagenes 
cv2.imshow("main",image)
cv2.imshow("HSV",imageHSV)
cv2.imshow("LAB",imageLab)
cv2.waitKey(0)


