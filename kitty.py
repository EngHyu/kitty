# coding=utf-8
from cv2 import *
import numpy as np
import os
class Keyboard:
    def __init__(self, user_id, keyboard_id, src, dst='./temp.jpg'):
        img_o    = imread(src)
        img_o    = self.detectMarker(img_o)

        rects_2d = self.detectRect(img_o)
        self.get_output(rects_2d, user_id, keyboard_id)
        #imwrite(dst, img_o)
        #self.show(img_m)
        #self.show(img_o)


    def detectMarker(self, img):
        img, corners, ids = self.processMarker(img)
        img = self.drawMarker(img, corners, ids)
        img = self.resizeMarker(img, corners, ids)
        return img

    def processMarker(self, img):
        aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_250)
        parameters =  aruco.DetectorParameters_create()

        corners, ids, _ = aruco.detectMarkers(img, aruco_dict, parameters=parameters)
        return img, corners, ids

    def drawMarker(self, img, corners, ids):
        img = aruco.drawDetectedMarkers(img, corners, ids)
        return img

    def resizeMarker(self, img, corners, ids):
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
        img         = self.get_processed_image(img)
        bound_rects = self.get_bound_rects(img)
        rects_1d    = self.get_rects_1d(bound_rects)
        rects_2d    = self.get_rects_2d(rects_1d)

        return rects_2d

    def get_processed_image(self, img):
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

            center = [x + w // 2, y + h // 2, w, h]
            rects_1d.append(center)

        rects_1d = sorted(rects_1d, key=lambda center: center[1])
        return rects_1d

    def get_rects_2d(self, rects_1d):
        rects_2d = self.get_line(rects_1d)
        rects_2d = self.remove_double(rects_2d)
        rects_2d = self.scale(rects_2d)
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
        for idx_line, line in enumerate(rects_2d):
            rects_2d[idx_line] = sorted(line, key=lambda center: center[0])

        new_rects_2d = rects_2d.copy()
        for idx_line, line in enumerate(rects_2d):
            p_rect = line[0]
            for rect in line[1:]:
                if rect[0] - p_rect[0] < p_rect[2] // 4:
                    new_rects_2d[idx_line].remove(rect)

                p_rect = rect

        return new_rects_2d

    def scale(self, rects_2d):
        for line in rects_2d:
            for rect in line:
                for idx_num, num in enumerate(rect):
                    rect[idx_num] = int(num / 500 * 2100)

        return rects_2d


    def get_output(self, rects, user_id='./sqlite3/220102/', keyboard_id=1):
        if not os.path.exists(user_id):
            os.mkdir(user_id)

        import json
        path = os.path.join(user_id, str(keyboard_id) + '.json')
        with open(path, 'w') as output:
            json.dump(rects, output)

    def drawRect(self, img, rects):
        for line in rects:
            for rect in line:
                circle(img, tuple(rect[:2]), 5, (255, 255, 255), -1)

        return img

    def show(self, img):
        imshow("Image", img)
        waitKey(0)


if __name__ == "__main__":
    keyboard = Keyboard("./9.png", "../10.png")
