from slamBackend.services.print import PrintService
from procotol.commonMessage import *
from procotol.slamDataMessage import *

class ServiceControler:

    def __init__(self) -> None:
        pass

    def startService(self, message):

        clientMessage = ClientMessage.loadJson(message)

        serType = clientMessage.type

        if serType == ServiceType.PRINT_SERVICE:

            res = PrintService(clientMessage).run()

            res = SlamRes(res)

        serverMessage = ServerMessage(ServiceType.PRINT_SERVICE, StatusType.STATUS_OK, res.dumpJson())

        return serverMessage.dumpJson()


