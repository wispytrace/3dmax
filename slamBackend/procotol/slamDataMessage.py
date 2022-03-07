import base64
import json


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

    def __init__(self, result):

        self.result = result


    def dumpJson(self):

        jsonDict = dict()

        jsonDict['result'] = self.result

        jsonStr = json.dumps(jsonDict)

        return jsonStr


    @staticmethod
    def loadJson(jsonStr):

        jsonDict = json.loads(jsonStr)

        result = jsonDict['result']

        slamRes = SlamRes(result)

        return slamRes



