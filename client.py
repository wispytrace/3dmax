import sys, os

sys.path.append(os.path.dirname(os.path.realpath(__file__)))

from slamFront.client import slamClient
from slamFront.frontService.modelService import ModelService
from procotol.commonMessage import *


if __name__ == '__main__':

    modelService = ModelService("demo1")

    myClient = slamClient.SlamClient(ServiceType.SLAM_SERVICE, modelService)

    myClient.excuteService()

