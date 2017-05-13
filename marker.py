import numpy as np
import cv2
import cv2.aruco as aruco


'''
    drawMarker(...)
        drawMarker(dictionary, id, sidePixels[, img[, borderBits]]) -> img
'''

aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_250)
print(aruco_dict)
# second parameter is id number
# last parameter is total image size
for i in range(4):
    img = aruco.drawMarker(aruco_dict, i, 28)
    cv2.imwrite("marker_" + str(i) + ".jpg", img)
