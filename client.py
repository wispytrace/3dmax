import sys, os

sys.path.append(os.path.dirname(os.path.realpath(__file__)))

from slamFront.client import slamClient
from slamFront.frontService.modelService import ModelService
from procotol.commonMessage import *


if __name__ == '__main__':

    testService = ModelService("demo1")

    myClient = slamClient.SlamClient(ServiceType.PRINT_SERVICE, testService)

    myClient.excuteService()

