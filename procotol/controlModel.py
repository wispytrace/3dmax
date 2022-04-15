import math
import json

class SimpleModel:

    def __init__(self, angle=0, speedUp=0, speedDown=0, upTime=0, downTime=0):
        
        self.angle = angle
        self.speedUp = speedUp
        self.speedDown = speedDown
        self.upTime = upTime
        self.downTime = downTime
        
        self.constrains = {
            'angle': (0, 2*math.pi),
            'speedUp': (0, 5),
            'speedDown': (0, 5),
            'upTime': (0, 5),
            'downTime': (0, 5)
        }

    @staticmethod
    def getConstrainsName(self):
        
        nameList = []

        for key, _ in self.constrains.items():
            nameList.apend(key)

        return nameList

    def dumpJson(self):

        jsonDict = dict()

        jsonDict['angle'] = self.angle

        jsonDict['speedUp'] = self.speedUp

        jsonDict['speedDown'] = self.speedDown

        jsonDict['upTime'] = self.upTime

        jsonDict['downTime'] = self.downTime

        jsonStr = json.dumps(jsonDict)

        return jsonStr

    @staticmethod
    def loadJson(jsonStr):

        jsonDict = json.loads(jsonStr)

        angle = jsonDict['angle']

        speedUp = jsonDict['speedUp']

        speedDown = jsonDict['speedDown']

        upTime = jsonDict['upTime']

        downTime = jsonDict['downTime']

        simpleModel = SimpleModel(angle, speedUp, speedDown, upTime, downTime)

        return simpleModel