# coding=utf-8

from cv2 import *
import numpy as np
class Keyboard:
    def __init__(self, src, dst):
        self.img_o = imread(src)
        self.img_z = np.zeros(self.img_o.shape, self.img_o.dtype)
        self.rects = []

        #img = self.normalize(self.img_o)
        img = self.img_o.copy()
        img_m = self.detectMarker(img.copy())
        img_r = self.detectRect(img_m)
        #self.show(img_m)
        self.show(img_r)
        #imwrite(dst, img)

    def detectMarker(self, img):
        img, corners, ids = self.processMarker(img)
        img = self.drawMarker(img, corners, ids)
        return img

    def processMarker(self, img):
        aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_250)
        parameters =  aruco.DetectorParameters_create()

        corners, ids, rejectedImgPoints = aruco.detectMarkers(img, aruco_dict, parameters=parameters)
        return img, corners, ids

    def drawMarker(self, img, corners, ids):
        img = aruco.drawDetectedMarkers(img, corners, ids)

        h, w  = img.shape[:2]
        h = round(500 / w * h)
        w = 500

        print(ids)
        for point in corners:
            print(point)

        src = np.array([
        corners[3][0][3],  #2
        corners[2][0][0],  #1
        corners[0][0][1],  #0
        corners[1][0][2]], #3
        dtype = "float32")

        dst = np.array([
        [0, 0],
    	[w, 0],
    	[w, h],
    	[0, h]],
        dtype = "float32")

        M   = getPerspectiveTransform(src, dst)
        img = warpPerspective(img, M, (w, h))
        return img

    def detectRect(self, img):
        img = self.processRect(img)
        img = self.drawRect(img)
        return img

    def processRect(self, img):
        img = cvtColor(img, COLOR_BGR2GRAY)
        img = Canny(img, 100, 300, 3)
        _, thresh = threshold(img, 200, 255, THRESH_BINARY)
        _, contours, hierarchy = findContours(thresh, RETR_TREE, CHAIN_APPROX_SIMPLE)
        boundRects = []

        for contour in contours:
            epsilon = 0.1 * arcLength(contour, True)
            approx = approxPolyDP(contour, epsilon, True)
            boundRects.append(boundingRect(approx))

        for boundRect in boundRects:
            x, y, w, h = boundRect
            ratio = h / w
            area  = h * w

            if ratio > 1.5:  continue
            if ratio < 0.5:  continue
            if area  > 5500: continue
            if area  < 300:  continue

            start  = (x, y)
            end    = (x + w, y + h)
            center = (x + w / 2, y + h / 2)
            self.rects.append((start, end, center))

        return img

    def drawRect(self, img):
        for index, rect in enumerate(self.rects):
            rectangle(img, rect[0], rect[1], (255, 255, 255), 3)

        return img

    def show(self, img):
        imshow("Image", img)
        waitKey(0)

if __name__ == "__main__":
    keyboard = Keyboard("/Users/roomedia/Desktop/9.png", "/Users/roomedia/Desktop/10.png")
