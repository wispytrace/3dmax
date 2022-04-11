import functools


class FrameKey:

    def __init__(self, fid, x, y, describe):
        self.fid = fid
        self.x = x
        self.y = y
        self.describe = describe


class MapPoint:

    def __init__(self, mId, fId):

        self.mId = mId
        self.refId = fId

        self.nearbyImg = None
        self.describe = None
        self.describeList = []
        self.frameKeyList = []


        self.gx = None
        self.gy = None

    def setDescribe(self, describe):

        self.describe = describe
        self.describeList.append(describe)

    def addSharedFrame(self, fId, x, y, describe):

        self.frameKeyList.append(FrameKey(fId, x, y, describe))

    def setGlobalXY(self, x, y):

        self.gx = x
        self.gy = y

    def setNearbyImg(self, img):

        self.nearbyImg = img

    def disposed(self, frameList):

        if len(self.frameKeyList) != 0:

            for match in self.frameKeyList:
                frameList[match.fid].mapPoints.remove(self.mId)

        del self

    def computeDistinctiveDescriptors(self):


        describeList = []

        for match in self.frameKeyList:
            describeList.append(match.describe)

        describeList.sort(key=functools.cmp_to_key(self.descCompare))

        self.describe = describeList[int(len(self.frameKeyList)/2)]

        return self.describe

    @staticmethod
    def descCompare(x, y):

        for i in range(len(x)):
            if x[i] > y[i]:
                return 1
            if x[i] < y[i]:
                return -1
        return 0

if __name__ == '__main__':

    des1 = [1 for i in range(256)]
    des2 = [0 for i in range(256)]

    des = []
    des.append(des1)
    des.append(des2)
    print(des)

    des.sort(key=functools.cmp_to_key(MapPoint.descCompare))
    print(des)