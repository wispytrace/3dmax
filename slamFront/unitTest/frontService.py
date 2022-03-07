
class FrontService:


    def __init__(self):
        pass

    def getData(self):

        data = "who am I"

        return data

    def callBack(self, res):

        print(res.dumpJson())

