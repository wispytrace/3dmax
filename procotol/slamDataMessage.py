import base64
import json
from procotol.controlModel import SimpleModel

class SlamData:

    def __init__(self, image):

        self.image = image

    def dumpJson(self):

        jsonDict = dict()

        image = base64.b64encode(self.image)

        image = image.decode("utf-8")

        jsonDict['image'] = image

        jsonStr = json.dumps(jsonDict)

        return jsonStr


    @staticmethod
    def loadJson(jsonStr):

        jsonDict = json.loads(jsonStr)

        image = jsonDict['image']

        image = image.encode("utf-8")

        image = base64.b64decode(image)

        slamData = SlamData(image)

        return slamData


class SlamRes:

    def __init__(self, comment, control):

        self.comment = comment

        self.control = control


    def dumpJson(self):

        jsonDict = dict()

        jsonDict['comment'] = self.comment

        jsonDict['control'] = self.control.dumpJson()

        jsonStr = json.dumps(jsonDict)

        return jsonStr


    @staticmethod
    def loadJson(jsonStr):

        jsonDict = json.loads(jsonStr)

        comment = jsonDict['comment']

        control = SimpleModel.loadJson(jsonDict['control'])

        slamRes = SlamRes(comment, control)

        return slamRes



