from slamBackend.services.slamServicePkg.edgeOperator.edge import Canny
from slamBackend.services.slamServicePkg.objectDetect.detect import Detector
from slamBackend.services.slamServicePkg.orbSlam.orbSlam import ORBSlam
from slamBackend.services.slamServicePkg.control.simpleControl import SimpleControl

from procotol.commonMessage import *
from procotol.slamDataMessage import *
from procotol.controlModel import SimpleModel
import numpy as np
import cv2 as cv


class SlamService:

    def __init__(self):

        self.edgeCheker = Canny()
        self.detector = Detector()
        self.orbSlam = ORBSlam()
        self.controlGenerator = SimpleControl(SimpleModel())

        self.detector.setTarget(cv.imread("H:\HkResearch\code\PythonRobotics\orbSlam\\target.jpg"))

    def initService(self, message):
        slamData = SlamData.loadJson(message.data)
        image = cv.imdecode(np.array(bytearray(slamData.image), dtype='uint8'), cv.IMREAD_UNCHANGED)
        image = cv.cvtColor(image, cv.COLOR_RGB2GRAY)
        self.detector.setTarget(image)
        self.orbSlam.setInitNode(self.orbSlam.getConstrain(0, 0))

        comment = "init Successful"
        control = SimpleModel()
        slamRes = SlamRes(comment, control)

        return StatusType.STATUS_OK, slamRes

    def runService(self, message):

        slamData = SlamData.loadJson(message.data)
        image = cv.imdecode(np.array(bytearray(slamData.image), dtype='uint8'), cv.IMREAD_UNCHANGED)
        cv.imwrite('test.jpg', image)
        image = cv.cvtColor(image, cv.COLOR_RGB2GRAY)

        edge = self.edgeCheker.check(image)
        x, y, _ = self.detector.detect(image, edge)
        self.orbSlam.receiveImg(image, x, y)
        self.orbSlam.reconstrcutGraph()
        self.orbSlam.printRobotPos()

        control = self.controlGenerator.getControl(x, y, x+10, y+10)
        self.orbSlam.graph.addRobotNode()

        comment = 'work well'
        slamRes = SlamRes(comment, control)


        return StatusType.STATUS_OK, slamRes

    def endService(self, message):

        raise GeneratorExit()

    def run(self, message):


        if message.command == CommandType.START_SERVICE:
            status, slamRes = self.initService(message)
        elif message.command == CommandType.RUNTIME_SERVICE:
            status, slamRes = self.runService(message)
        elif message.command == CommandType.END_SERVICE:
            status, slamRes = self.endService(message)
        else:
            status = StatusType.STATUS_ERROR
            comment = 'undefined command'
            control = SimpleModel()
            slamRes = SlamRes(comment, control)
            print('undefined command!')

        return status, slamRes



