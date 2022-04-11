
class Frame:

    def __init__(self, fId, mvImagePyramid=None, keyPoints=None):

        self.fId = fId
        self.mvImagePyramid = mvImagePyramid
        self.keyPoints = keyPoints
        self.nlevels = 0 if keyPoints == None else len(keyPoints)

        self.mapPoints = []
        # self.gx = None
        # self.gy = None

    def addMapPoint(self, mapId):

        self.mapPoints.append(mapId)

    def disposed(self, mapPointsList):

        for mId in self.mapPoints:
            mapPoint = mapPointsList[mId]
            for match in mapPoint.frameKeyList:
                if match.fid == self.fId:
                    mapPoint.matchs.remove(match)
                    break
        del self


