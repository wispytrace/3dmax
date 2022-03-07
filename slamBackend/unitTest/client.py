from client import slamClient
from slamFront.unitTest.frontService import FrontService

if __name__ == '__main__':

    testService = FrontService()

    myClient = slamClient.SlamClient(ServiceType.PRINT_SERVICE, testService)

    myClient.excuteService()

