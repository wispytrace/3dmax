
from pymxs import runtime as rt
from slamFront.utlis.camera import RuntimeCamera
from slamFront.utlis.plant import RuntimePlant
from slamFront.frontService.config import ModelConfig
from procotol.slamDataMessage import *
from procotol.commonMessage import *
import time

class ModelService():


    def __init__(self, modelName):

        self.modelName = modelName

        modelPath, camPos, objPos, plantPos, plantRadius, outputPath = self.loadConfig()

        self.runtimeCamera = RuntimeCamera()

        self.runtimeCamera.setPose(camPos=rt.point3(camPos[0], camPos[1], camPos[2]), objPos=rt.point3(objPos[0], objPos[1], objPos[2]))

        self.runtimePlant = RuntimePlant(initPos=rt.point3(plantPos[0], plantPos[1], plantPos[2]), initRadius=rt.point3(plantRadius[0], plantRadius[1], plantRadius[2]))

        self.outputPath = outputPath

        rt.resetMaxFile(rt.name('noPrompt'))

        rt.loadMaxFile(modelPath)

        rt.redrawViews()


    def loadConfig(self):

        modelPath = ModelConfig[self.modelName]['path']

        camPos = ModelConfig[self.modelName]['camPos']

        objPos = ModelConfig[self.modelName]['objPos']

        plantPos = ModelConfig[self.modelName]['plantPos']

        plantRadius = ModelConfig[self.modelName]['plantRadius']

        outputPath = ModelConfig[self.modelName]['outputPath']

        return modelPath, camPos, objPos, plantPos, plantRadius, outputPath


    def getData(self):

        self.runtimeCamera.getFrame(outputPath=self.outputPath)

        with open(self.outputPath, "rb") as f:

            data = f.read()

        slamData = SlamData(data)

        strData = slamData.dumpJson()

        return strData


    def callBack(self, res):

        if res.status != StatusType.STATUS_OK:

            raise Exception("backend service error!")

        slamRes = SlamRes.loadJson(res.data)

        print(slamRes.result)

        time.sleep(2)
