from slamBackend.services.slamServicePkg.edgeOperator.edge import Canny
from slamBackend.services.slamServicePkg.objectDetect.detect import Detector
from slamBackend.services.slamServicePkg.orbSlam.orbSlam import ORBSlam
from procotol.commonMessage import *
from procotol.slamDataMessage import *
import numpy as np
import cv2 as cv


class SlamService:

    def __init__(self):

        self.edgeCheker = Canny()
        self.detector = Detector()
        self.orbSlam = ORBSlam()

        self.detector.setTarget(cv.imread("H:\HkResearch\code\PythonRobotics\orbSlam\\target.jpg"))

    def initService(self, message):


        return StatusType.STATUS_OK, "init Successful"

    def runService(self, message):

        slamData = SlamData.loadJson(message.data)
        image = cv.imdecode(np.array(bytearray(slamData.image), dtype='uint8'), cv.IMREAD_UNCHANGED)
        cv.imwrite('test.jpg', image)
        image = cv.cvtColor(image, cv.COLOR_RGB2GRAY)
        mvImagePyramid, keyPoints = self.orbSlam.extractImgFeature(image)

        return StatusType.STATUS_CLOSE, "run Successful"

    def endService(self, message):

        return "end Successful"

    def run(self, message):


        if message.command == CommandType.START_SERVICE:
            status, res = self.initService(message)
        elif message.command == CommandType.RUNTIME_SERVICE:
            status, res = self.runService(message)
        elif message.command == CommandType.END_SERVICE:
            status, res = self.endService(message)
        else:
            status = StatusType.STATUS_ERROR
            res = 'undefined command'
            print('undefined command!')

        return status, res





