import cv2

from slamBackend.services.slamServicePkg.orbSlam.featureEx.orbExtractor import ORBExtractor
from slamBackend.services.slamServicePkg.orbSlam.mapInfo.frame import Frame
from slamBackend.services.slamServicePkg.orbSlam.mapInfo.mapPoint import MapPoint
from slamBackend.services.slamServicePkg.orbSlam.graphOptimizer.graph import Graph
import math
import numpy as np
import matplotlib.pyplot as plt
import time

class ORBSlam:

    def __init__(self):

        self.orbExtractor = ORBExtractor()
        self.graph = Graph()

        self.fIdRecord = 0
        self.mIdRecord = 0
        self.desMatchGate = 25
        self.preciseMatchWindow = 16
        self.preciseDisGate = 1.5

        self.frameList = dict()
        self.mapPointList = dict()

        self.NO_FRAME_ID = 0

    def getFid(self):

        fid = self.fIdRecord
        self.fIdRecord += 1

        return fid

    def getMid(self):

        mid = self.mIdRecord
        self.mIdRecord += 1

        return mid

    def calDescDistance(self, desc1, desc2):

        distance = 0
        for i in range(len(desc1)):
            if desc2[i] != desc1[i]:
                distance += 1
        return distance

    def roughlyMatch(self, keyPoints, mapPoints):

        matched = []

        for key, value in mapPoints.items():
            dis = 256
            matchIndx = None
            for i in range(len(keyPoints)):
                for j in range(len(keyPoints[i])):
                    keyPoint = keyPoints[i][j]
                    d = self.calDescDistance(value.describe, keyPoint.describe)
                    if dis > d and d < self.desMatchGate:
                        dis = d
                        matchIndx = (i, j)

            if matchIndx is not None:
                matched.append({'mapPoint': key, 'keyPoint': matchIndx})

        return matched

    def preciseMatch(self, img1, img2):
        dis = 0
        for i in range(0, self.preciseMatchWindow*2+1):
            for j in range(0, self.preciseMatchWindow*2+1):
                piex1 = int(img1[i][j])
                piex2 = int(img2[i][j])
                dis += math.fabs(piex2 - piex1)

        dis = dis / ((self.preciseMatchWindow*2+1)**2)

        return dis

    def keyToMapMatch(self, frame):

        if len(self.mapPointList) == 0:
            return []

        keyPoints = frame.keyPoints
        roughMatched = self.roughlyMatch(keyPoints, self.mapPointList)

        globalDis = []
        for i in range(len(roughMatched)):
            level, index = roughMatched[i]['keyPoint']
            mapPoint = self.mapPointList[roughMatched[i]['mapPoint']]
            keyPoint = keyPoints[level][index]
            keyImg = frame.mvImagePyramid[level][keyPoint.y-self.preciseMatchWindow: keyPoint.y+self.preciseMatchWindow+1,
                     keyPoint.x-self.preciseMatchWindow: keyPoint.x+self.preciseMatchWindow+1]
            mapImg = mapPoint.nearbyImg
            dis = self.preciseMatch(keyImg, mapImg)
            globalDis.append(dis)
        meanDis = np.mean(globalDis)

        precisedMatched = []
        for i in range(len(roughMatched)):
            if globalDis[i] > meanDis*self.preciseDisGate:
                continue
            else:
                precisedMatched.append(roughMatched[i])

        return precisedMatched

    def setFrameConstarin(self, frame, targetX, targetY):

        for mid in frame.mapPoints:

            for frameKey in self.mapPointList[mid].frameKeyList:
                if frameKey.fid == frame.fId:
                    x = frameKey.x
                    y = frameKey.y
                    break

            x -= targetX
            y -= targetY
            constrain = self.graph.getConstrain(x, y)
            self.graph.addLandMarkNode(constrain, mid)

    def receiveImg(self, img, targetX, targetY):

        mvImagePyramid, keyPoints = self.orbExtractor.extractImgFeature(img)
        fid = self.getFid()
        frame = Frame(fid, mvImagePyramid, keyPoints)
        self.frameList[fid] = frame

        matches = self.keyToMapMatch(frame)

        for item in matches:
            mapPoint = self.mapPointList[item['mapPoint']]
            level, index = item['keyPoint']
            keyPoint = keyPoints[level][index]
            x, y = self.orbExtractor.resumeImgPostion(keyPoint.x, keyPoint.y, level)
            mapPoint.addSharedFrame(fid, x, y, keyPoint.describe)
            mapPoint.computeDistinctiveDescriptors()
            frame.addMapPoint(item['mapPoint'])

        for i in range(self.orbExtractor.nlevels):
            for j in range(len(frame.keyPoints[i])):
                isCreate = True

                for item in matches:
                    level, index = item['keyPoint']
                    if level == i and index == j:
                        isCreate = False
                        break

                if not isCreate:
                    continue
                keyPoint = frame.keyPoints[i][j]
                x, y = self.orbExtractor.resumeImgPostion(keyPoint.x, keyPoint.y, i)
                mid = self.getMid()
                mapPoint = MapPoint(mid, fid)
                mapPoint.addSharedFrame(fid, x, y, keyPoint.describe)
                mapPoint.computeDistinctiveDescriptors()
                keyImg = frame.mvImagePyramid[i][
                         keyPoint.y - self.preciseMatchWindow: keyPoint.y + self.preciseMatchWindow + 1,
                         keyPoint.x - self.preciseMatchWindow: keyPoint.x + self.preciseMatchWindow + 1]
                mapPoint.nearbyImg = keyImg

                self.mapPointList[mid] = mapPoint
                frame.addMapPoint(mid)

        self.setFrameConstarin(frame, targetX, targetY)

    def reconstrcutGraph(self):

        self.graph.reconstrcutGraph()

    def solveIncGraph(self):

        self.graph.solveIncGraph()

    def getConstrain(self, x, y):

        return self.graph.getConstrain(x, y)

    def extractImgFeature(self, img):

        return self.orbExtractor.extractImgFeature(img)

# debug code
#
    def createMap(self, img):
        mvImagePyramid, keyPoints = self.orbExtractor.extractImgFeature(img)

        for i in range(self.orbExtractor.nlevels):
            for j in range(len(keyPoints[i])):

                mid = self.getMid()
                keyPoint = keyPoints[i][j]
                x, y = self.orbExtractor.resumeImgPostion(keyPoint.x, keyPoint.y, i)
                mapPoint = MapPoint(mid, self.NO_FRAME_ID)
                mapPoint.describe = keyPoint.describe
                mapPoint.gx = x
                mapPoint.gy = y
                keyImg = mvImagePyramid[i][
                         keyPoint.y - self.preciseMatchWindow: keyPoint.y + self.preciseMatchWindow + 1,
                         keyPoint.x - self.preciseMatchWindow: keyPoint.x + self.preciseMatchWindow + 1]
                mapPoint.nearbyImg = keyImg
                self.mapPointList[mid] = mapPoint
        self.frameList[self.NO_FRAME_ID] = Frame(self.NO_FRAME_ID, mvImagePyramid, keyPoints)

    def saveMap(self, filePath='map.sm'):

        with open(filePath, 'wb') as f:

            length = len(self.mapPointList)
            f.write(length.to_bytes(4, byteorder='big'))

            for k, mp in self.mapPointList.items():
                gx = mp.gx
                gy = mp.gy
                describe = mp.describe
                img = mp.nearbyImg

                f.write(gx.to_bytes(4, byteorder='big'))
                f.write(gy.to_bytes(4, byteorder='big'))

                count = 0
                for i in range(1, len(describe)+1):

                    left = (i-1) % 32
                    count = count + describe[i-1] * (2**left)

                    if i % 32 == 0:
                        f.write(count.to_bytes(4, byteorder='big'))
                        count = 0

                for i in range(0, self.preciseMatchWindow*2+1):
                    for j in range(0, self.preciseMatchWindow*2+1):
                        pixel = int(img[i][j])
                        f.write(pixel.to_bytes(1, byteorder='big'))

            f.flush()

    def loadMap(self,  filePath='map.sm'):

        with open(filePath, 'rb') as f:
            length = f.read(4)
            length = int.from_bytes(length, byteorder='big')
            for i in range(length):

                gx = int.from_bytes(f.read(4), byteorder='big')
                gy = int.from_bytes(f.read(4), byteorder='big')

                describe = []
                for j in range(8):
                    dj = int.from_bytes(f.read(4), byteorder='big')
                    for k in range(32):
                        describe.append(dj & 1)
                        dj = int(dj / 2)

                img = np.zeros((self.preciseMatchWindow*2+1, self.preciseMatchWindow*2+1), dtype=np.uint8)
                for i in range(0, self.preciseMatchWindow*2+1):
                    for j in range(0, self.preciseMatchWindow*2+1):
                        img[i][j] = int.from_bytes(f.read(1), byteorder='big')

                mid = self.getMid()

                mapPoint = MapPoint(mid, self.NO_FRAME_ID)
                mapPoint.gx = gx
                mapPoint.gy = gy
                mapPoint.describe = describe
                mapPoint.nearbyImg = img
                self.mapPointList[mid] = mapPoint



    def showImg(self):

        for i in range(len(self.frameList)):

            plt.figure(i)
            plt.imshow(self.frameList[i].mvImagePyramid[0])
            ox = []
            oy = []
            for keyPoint in self.frameList[i].keyPoints[0]:
                ox.append(keyPoint.x)
                oy.append(keyPoint.y)
            plt.scatter(ox, oy, s=2)
            mx = []
            my = []
            for j in range(len(self.mapPointList)):
                if len(self.mapPointList[j].frameKeyList) < 2:
                    continue
                else:
                    for frameKey in self.mapPointList[j].frameKeyList:
                        if frameKey.fid == self.frameList[i].fId:
                            x = frameKey.x
                            y = frameKey.y
                            break
                    x += self.orbExtractor.borderWidth
                    y += self.orbExtractor.borderWidth
                    mx.append(x)
                    my.append(y)

            plt.scatter(mx, my, s=5, marker='x')

        plt.show()

if __name__ == '__main__':

    im1 = cv2.imread('H:\HkResearch\code\PythonRobotics\orbSlam\\r1.jpg', 0)
    im2 = cv2.imread('H:\HkResearch\code\PythonRobotics\orbSlam\\r2.jpg', 0)
    start = time.time()
    orb = ORBSlam()
    # cons = orb.graph.getConstrain(0, 0)
    # orb.graph.setInitNode(cons)
    # orb.receiveImg(im1, 0, 0)
    # k = len(orb.mapPointList) + 1
    # orb.graph.addRobotNode(orb.graph.getConstrain(295, -165))
    # # orb.graph.addRobotNode()
    # orb.receiveImg(im2, 0, 0)
    # orb.graph.reconstrcutGraph()
    # end = time.time()
    # print(orb.graph.position[k])
    # print(end-start)
    # orb.showImg()
    # print(len(orb.mapPointList))
    img = cv2.imread('H:\code\\3dmax\\test.jpg', 0)
    orb.createMap(img)
    print(orb.mapPointList[0].gx, orb.mapPointList[0].gy, orb.mapPointList[0].describe, orb.mapPointList[0].nearbyImg)
    k = len(orb.mapPointList)
    orb.saveMap()
    orb.loadMap()
    print(orb.mapPointList[k].gx, orb.mapPointList[k].gy, orb.mapPointList[k].describe, orb.mapPointList[k].nearbyImg)

