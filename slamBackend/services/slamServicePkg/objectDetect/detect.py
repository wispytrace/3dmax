import numpy
import cv2 as cv
import skimage.io
import skimage.feature
import skimage.color
import skimage.transform
import skimage.util
import skimage.segmentation
import time


class Detector:

    def __init__(self):

        self.target = None
        self.fxRate = 0.5

        self.hashWidth = 32
        self.hashHeight = 32

    def setTarget(self, img):

        self.target = img

    def serEdgeChecker(self, check):

        self.edgeChecker = check

    def _generate_segments(self, img):

        h, w = img.shape
        im_mask = numpy.zeros(img.shape[:2])
        label = 1
        for i in range(h):
            for j in range(w):
                if im_mask[i][j] != 0 or img[i][j] == 0:
                    continue
                else:
                    # im_mask[i][j] = label
                    neighbours = [(j, i)]
                    while len(neighbours) != 0:
                        xy = neighbours.pop()
                        x = xy[0]
                        y = xy[1]
                        if x >= 0 and y >= 0 and x < w and y < h and im_mask[y][x] == 0 and img[y][x] > 0:
                            im_mask[y][x] = label
                            neighbours.extend([(x+u, y+v) for u in (-1, 0, 1) for v in (-1, 0, 1)])
                    label = label + 1

        return im_mask

    def _merge_regions(self, regions):

        R = list(regions.items())
        for cur, a in enumerate(R[:-1]):
            for b in R:
                if (a[1]["min_x"] >= b[1]["min_x"] and a[1]["max_x"] <= b[1]["max_x"]) and a[1]["min_y"] >= b[1]["min_y"] and a[1]["max_y"] <= b[1]["max_y"] and a[1] != b[1]:
                    del regions[a[0]]
                    break

        return regions

    def _extract_regions(self, img):

        R = {}

        # pass 1: count pixel positions
        for y, i in enumerate(img):

            for x,  l in enumerate(i):

                if l == 0:
                    continue
                # initialize a new region
                if l not in R:
                    R[l] = {
                        "min_x": 0xffff, "min_y": 0xffff,
                        "max_x": 0, "max_y": 0, "labels": [l]}

                # bounding box
                if R[l]["min_x"] > x:
                    R[l]["min_x"] = x
                if R[l]["min_y"] > y:
                    R[l]["min_y"] = y
                if R[l]["max_x"] < x:
                    R[l]["max_x"] = x
                if R[l]["max_y"] < y:
                    R[l]["max_y"] = y

        return R


    def getDiff(self, image):  # 将要裁剪成w*h的image照片 得到渐变序列
        diff = []
        im = cv.resize(image, dsize=(self.hashHeight, self.hashWidth))
        imgray = cv.cvtColor(im, cv.COLOR_RGB2GRAY)

        for row in range(self.hashHeight):
            for col in range(self.hashWidth - 1):
                left = imgray[row][col]  # 当前位置号
                right = imgray[row][col+1]
                diff.append(left > right)
        return diff

    def getHamming(self, diff=[], diff2=[]):
        # print len(diff)
        hamming_distance = 0
        for i in range(len(diff)):
            if diff[i] != diff2[i]:
                hamming_distance += 1
        return hamming_distance

    def detect(self, img, imgEdge):

        if self.target is None:
            print("Please load target first!")
            return
        imgEdge = cv.resize(imgEdge, None, fx=self.fxRate, fy=self.fxRate)

        img_mask = self._generate_segments(imgEdge)
        regions = self._extract_regions(img_mask)

        scoreList = []
        targetDiff = self.getDiff(self.target)

        for k, v in regions.items():
            v['min_x'] = int(v['min_x'] / self.fxRate)
            v['min_y'] = int(v['min_y'] / self.fxRate)
            v['max_x'] = int(v['max_x'] / self.fxRate)
            v['max_y'] = int(v['max_y'] / self.fxRate)
            cropedImg = img[v['min_y']:v['max_y'], v['min_x']:v['max_x']]
            h, w = cropedImg.shape[:2]
            if h == 0 or w == 0:
                continue
            diff = self.getDiff(cropedImg)
            score = self.getHamming(diff, targetDiff)
            scoreList.append((k, score))

        if len(scoreList) == 0:
            print("No regions to detect")
            return

        scoreList.sort(key=lambda x: x[1])
        rect = regions[scoreList[0][0]]

        # self.showRegions(regions, img)

        return rect['min_x'], rect['min_y'], rect['max_x'], rect['max_y']

    def showRegions(self, regions, img):

        for k,v in regions.items():
            img = cv.rectangle(img, (v['min_x'], v['min_y']), (v['max_x'], v['max_y']), (0, 255, 0), 1)
        cv.imshow('rect', img)


# if __name__ == '__main__':
#     stat = time.time()
#     img = cv.imread('H:\HkResearch\code\PythonRobotics\orbSlam\\r1.jpg')
#     target = cv.imread("H:\HkResearch\code\PythonRobotics\orbSlam\\target.jpg")
#
#     detector = Detector(target)
#     imgEdge = Canny().check(img)
#     x0, y0, x1, y1 = detector.detect(img, imgEdge)
#     img = cv.rectangle(img, (x0, y0), (x1, y1), (0, 0, 255), 1)
#     end = time.time()
#
#     print(end-stat)
#
#     cv.imshow("img", img)
#     cv.waitKey(0)
