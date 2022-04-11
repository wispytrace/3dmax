from slamBackend.services.print import PrintService
from slamBackend.services.slam import SlamService

from procotol.commonMessage import *
from procotol.slamDataMessage import *

class ServiceControler:

    def __init__(self) -> None:
        self.service = None

    def startService(self, message):

        clientMessage = ClientMessage.loadJson(message)

        serType = clientMessage.type

        if serType == ServiceType.PRINT_SERVICE:

            res = PrintService(clientMessage).run()

            res = SlamRes(res)
        elif serType == ServiceType.SLAM_SERVICE:

            if self.service is None:
                self.service = SlamService()

            status, res = self.service.run(clientMessage)

            res = SlamRes(res)

        serverMessage = ServerMessage(ServiceType.PRINT_SERVICE, status, res.dumpJson())

        return serverMessage.dumpJson()


