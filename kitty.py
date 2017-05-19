# coding=utf-8
from cv2 import *
import numpy as np
class Keyboard:
    def __init__(self, src, dst):
        self.img_o = imread(src)

        img_o = self.img_o.copy()
        img_m = self.detectMarker(img_o)
        img_r = self.detectRect(img_m)
        #self.show(img_m)
        #self.show(img_r)
        imwrite(dst, img_r)

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
        img = self.get_image(img)

        bound_rects = self.get_bound_rects(img)
        rects_1d    = self.get_rects_1d(bound_rects)
        rects_2d    = self.get_rects_2d(rects_1d)
        space_bar   = self.get_space_bar(rects_1d)

        img = self.drawRect(img, rects_2d)
        self.get_output(rects_2d)

        return img

    def get_image(self, img):
        img = cvtColor(img, COLOR_BGR2GRAY)
        img = Canny(img, 100, 300, 3)

        return img

    def get_bound_rects(self, img):
        _, img = threshold(img, 200, 255, THRESH_BINARY)
        _, contours, _ = findContours(img, RETR_TREE, CHAIN_APPROX_SIMPLE)

        boundRects = list()
        for contour in contours:
            epsilon = 0.1 * arcLength(contour, True)
            approx = approxPolyDP(contour, epsilon, True)
            boundRects.append(boundingRect(approx))

        return boundRects

    def get_rects_1d(self, boundRects):
        rects_1d = list()
        for boundRect in boundRects:
            x, y, w, h = boundRect
            ratio = h / w
            area  = h * w

            if ratio > 1.3:  continue
            if ratio < 0.2:  continue
            if area  > 5500: continue
            if area  < 300:  continue

            start  = (x, y)
            end    = (x + w, y + h)
            center = (x + w // 2, y + h // 2)
            rects_1d.append(center + boundRect[2:])

        rects_1d = sorted(rects_1d, key=lambda center: center[1])
        return rects_1d

    def get_rects_2d(self, rects_1d):
        rects_2d = self.get_line(rects_1d)
        rects_2d = self.remove_double(rects_2d)
        return rects_2d

    def get_line(self, rects_1d):
        rects_2d = [[rects_1d[0]]]
        for i in range(len(rects_1d) - 1):
            this_rect = rects_1d[i]
            next_rect = rects_1d[i+1]

            if next_rect[1] - this_rect[1] < this_rect[3] // 2:
                rects_2d[len(rects_2d) - 1].append(next_rect)
            else:
                rects_2d.append([next_rect])

        return rects_2d

    def remove_double(self, rects_2d):
        for index, line in enumerate(rects_2d):
            rects_2d[index] = sorted(line, key=lambda center: center[0])

        new_rects_2d = rects_2d.copy()
        for idx, line in enumerate(rects_2d):
            p_rect = line[0]
            for rect in line[1:]:
                if rect[0] - p_rect[0] < p_rect[2] // 4:
                    new_rects_2d[idx].remove(rect)

                p_rect = rect

        return new_rects_2d

    def get_space_bar(self, rects_1d):
        min_ratio = 2
        min_ratio_index = None

        for index, rect in enumerate(rects_1d):
            x, y, w, h = rect
            ratio = h / w

            if min_ratio <= ratio: continue
            min_ratio = ratio
            min_ratio_index = index

        return min_ratio_index

    def get_output(self, rects):
        with open("./layout.txt", "w+") as f:
            for line in rects:
                f.write(str(len(line)) + "\n")
                for rect in line:
                    f.write(str(rect) + "\n")
                f.write("\n")

    def drawRect(self, img, rects):
        for line in rects:
            for rect in line:
                circle(img, rect[:2], 5, (255, 255, 255), -1)

        return img

    def show(self, img):
        imshow("Image", img)
        waitKey(0)

if __name__ == "__main__":
    keyboard = Keyboard("/Users/roomedia/Desktop/9.png", "/Users/roomedia/Desktop/develop/df/10.png")
