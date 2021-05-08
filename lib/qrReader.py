import cv2
from pyzbar import pyzbar


def getQRS(img):
    return [{
        'polygon': QR.polygon,
        'rect': QR.rect,
        'text': QR.data.decode('utf-8')
    }
        for QR in pyzbar.decode(img)]




# EXAMPLE

# img = cv2.imread('./Codigo QR R2.png')
# imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
# for QR in getQRS(img):
#     print("The QR DATA", QR)
