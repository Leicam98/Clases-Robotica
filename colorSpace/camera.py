import cv2
import numpy as np

cv2.namedWindow("original")
cv2.namedWindow("filtered")

def callback(x):
    pass

cv2.createTrackbar("minH", "original", 0, 255, callback)
cv2.createTrackbar("maxH", "original", 0, 255, callback)

# si el argumento es int, se conecta a la webcam integrada (0) o la USB (1)
cam = cv2.VideoCapture(0)

while cam.isOpened():
    r, frame= cam.read()
    cv2.imshow("original", frame)
    minH = cv2.getTrackbarPos("minH", "original")
    maxH = cv2.getTrackbarPos("maxH", "original")

    minHSV = np.array([minH, 0, 0])
    maxHSV = np.array([maxH, 255, 255])

    imageHSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    mask = cv2.inRange(imageHSV, minHSV, maxHSV)
    cv2.imshow("filtered", mask)

    key = cv2.waitKey(1)
    if key==ord("q"): break

cv2.DestroyAllWindows()