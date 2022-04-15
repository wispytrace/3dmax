from slamBackend.services.print import PrintService
from slamBackend.services.slam import SlamService

from procotol.commonMessage import *
from procotol.slamDataMessage import *

class ServiceControler:

    def __init__(self) -> None:
        self.service = None

    def runService(self, message):

        clientMessage = ClientMessage.loadJson(message)

        serType = clientMessage.type

        if serType == ServiceType.PRINT_SERVICE:

            status = StatusType.STATUS_OK

            strRes = PrintService(clientMessage).run()

        elif serType == ServiceType.SLAM_SERVICE:

            if self.service is None:
                self.service = SlamService()

            status, res = self.service.run(clientMessage)
            strRes = res.dumpJson()

        serverMessage = ServerMessage(serType, status, strRes)

        strServerMessage = serverMessage.dumpJson()

        return strServerMessage


