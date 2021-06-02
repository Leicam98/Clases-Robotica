import cv2
import numpy as np
import math

def getPCAmatrix(binaryImage):
    #Para calcular la matriz de covarianza para PCA:
    data_points = []
    threshold = 0
    H = binaryImage.shape[0]
    W = binaryImage.shape[1]

    for i in range(H):
        for j in range(W):
            if binaryImage[i, j] > threshold:
                data_points.append([i, j])
    data_points = np.asarray(data_points)
    covMatrix = np.cov(data_points.T) 
    return covMatrix

#Lectura de imagen
image = cv2.imread("blueGiro.png")
#Conversion a HSV
imageHSV = cv2.cvtColor(image,cv2.COLOR_BGR2HSV)


#filtrado
#se utilizo filterHSV.py para definir los valores
minH = np.array([1,0,0])
maxH = np.array([125,255,255])
binaryImage = cv2.inRange(imageHSV,minH,maxH)
cv2.imwrite("img_binary.png",binaryImage)


#Calculo de los momentos
moments = cv2.moments(binaryImage,True)


#Area Objeto 
areaObject = moments['m00']
print("Area objeto:",areaObject)

#Area Imagen
areaImage = binaryImage.shape[0]*binaryImage.shape[1]
print("Area Imagen:", areaImage)

#Centro de masa
xcenter = moments['m10'] / moments['m00']
ycenter = moments['m01'] / moments['m00']

print("Area normalizada:",round(areaObject/areaImage,5))

#Posiciones normalizadas:
xnorm = xcenter/binaryImage.shape[0]
ynorm = ycenter/binaryImage.shape[1]
print("CM(x,y):", round(xnorm,5),round(ynorm,5))


marca_centro_objeto = cv2.circle(image,(int(xcenter), int(ycenter)), 3, (0,0,255), 4) 

cv2.putText(marca_centro_objeto, f"(x:{round(xnorm,5)}, y:{round(ynorm,5)})" ,(int(xcenter),int(ycenter+20)),cv2.FONT_HERSHEY_SIMPLEX, 0.5,(0,0,0),1)

#Llama funcion para hallar la matrix de covarianza PCA
covM = getPCAmatrix(binaryImage)

#Eigenvectors y eigenvalues de la matriz de covarianza
eig_val, eig_vec = np.linalg.eig(covM)

#eig_val es un vector de los eigenvalues
#eig_vect es una matriz cuyas columnas son los eigenvectores

#Posicion del mayor eigenvalue
pos = np.where(eig_val == max(eig_val))[0]
print(pos)

#El componente principal será el eigenvector que corresponde al mayor eigenvalue,
PC1 = eig_vec[:,pos] #Componente principal, vector normalizado
print("Componente Principal:", PC1)
 #

#Para hallar al angulo que forma con el eje x:
angulo = math.atan((PC1[0]/PC1[1]))
angulo = angulo*180/np.pi
angulo = round(angulo,5)

print("EL ANGULO ES", angulo )

#Para la recta en la direccion de la componente principal:
m = math.tan(angulo*np.pi/180) #pendiente
y1 =m*(0-xcenter)+ycenter #para x=0 P1(0,y1) 
x2 = (0-ycenter)/m+ xcenter #para y=0 P2(x2,0)

pt1= (0,int(y1))
pt2=(int(x2),0)


result=cv2.line(marca_centro_objeto,pt1,pt2,(0,0,255),2)
cv2.imshow("Result",result)
cv2.imwrite("Result.png",result)


#Sistema de referencia:
# 0---------------> X
# |
# |
# |
# |
# |
# |
# v Y

key=cv2.waitKey(0)
cv2.destroyAllWindows();