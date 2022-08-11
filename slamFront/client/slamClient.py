import socket
from slamFront.client import config
from procotol.commonMessage import *

class SlamClient:

    def __init__(self, serviceType, frontService):

        self.clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.clientSocket.connect((config.serverIP, config.serverPort))

        self.serviceType = serviceType

        self.frontService = frontService


    def initService(self):


        strData = self.frontService.getData("H:\code\\3dmax\\target.jpg")


        clientMessage = ClientMessage(self.serviceType, CommandType.START_SERVICE, strData)

        clientMessage = clientMessage.dumpJson().encode('utf-8')

        self.clientSocket.send(clientMessage)

        res = self.clientSocket.recv(config.maxBuffSize)

        res = ServerMessage.loadJson(res.decode("utf-8"))

        print(res.data)

        if res.status == StatusType.STATUS_ERROR:

            e = Exception('init failed please reconnect')

            raise e


    def excuteService(self):

        self.initService()

        while(True):

            strData = self.frontService.getData(self.frontService.outputPath)

            clientMessage = ClientMessage(self.serviceType, CommandType.RUNTIME_SERVICE, strData)

            clientMessage = clientMessage.dumpJson().encode('utf-8')

            self.clientSocket.send(clientMessage)

            res = self.clientSocket.recv(config.maxBuffSize)

            res = ServerMessage.loadJson(res.decode("utf-8"))

            if res.status == StatusType.STATUS_ERROR:

                raise Exception('backend service error please reconnect!')

            if res.status == StatusType.STATUS_CLOSE:

                print("slamServer has closed connect!")
                return

            self.frontService.callBack(res.data)




