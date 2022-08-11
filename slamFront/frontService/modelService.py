
from pymxs import runtime as rt
from slamFront.utlis.camera import RuntimeCamera
from slamFront.utlis.plant import RuntimePlant
from slamFront.frontService.config import ModelConfig
from procotol.slamDataMessage import *
from procotol.commonMessage import *
from procotol.controlModel import *

import time

class ModelService():


    def __init__(self, modelName):

        self.modelName = modelName

        self.outputPath = ModelConfig[self.modelName]['outputPath']

        self.sampleTime = ModelConfig[self.modelName]['sampleTime']

        modelPath = ModelConfig[self.modelName]['path']

        camPos = ModelConfig[self.modelName]['camPos']

        objPos = ModelConfig[self.modelName]['objPos']

        plantPos = ModelConfig[self.modelName]['plantPos']

        plantRadius = ModelConfig[self.modelName]['plantRadius']

        rt.resetMaxFile(rt.name('noPrompt'))

        rt.loadMaxFile(modelPath)

        self.runtimeCamera = RuntimeCamera()

        self.runtimeCamera.setPose(camPos=rt.point3(camPos[0], camPos[1], camPos[2]), objPos=rt.point3(objPos[0], objPos[1], objPos[2]))

        self.runtimePlant = RuntimePlant(initPos=rt.point3(plantPos[0], plantPos[1], plantPos[2]), initRadius=plantRadius)

        rt.redrawViews()

        





    def getData(self, path):

        self.runtimePlant.hideTraces()
        self.runtimeCamera.getFrame(outputPath=self.outputPath)
        self.runtimePlant.showTraces()
        with open(path, "rb") as f:

            data = f.read()

        slamData = SlamData(data)

        strData = slamData.dumpJson()

        return strData


    def getNextPosition(self, sx, sy, control):

        distance = 1 / 2 * control.speedUp * (control.upTime ** 2) + 1 / 2 * control.speedDown * (
                    control.speedUp * control.upTime / control.speedDown) ** 2
        deg = control.angle
        x = sx + math.cos(deg) * distance
        y = sy + math.sin(deg) * distance

        return x, y

    def callBack(self, res):

        slamRes = SlamRes.loadJson(res)

        control = slamRes.control

        x, y = self.getNextPosition(0, 0, control)

        self.runtimePlant.doMove(rt.Point3(x, y, 0)+self.runtimePlant.currentPos)

        print(slamRes.comment)

        time.sleep(self.sampleTime)
