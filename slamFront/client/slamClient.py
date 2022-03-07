import socket
from slamBackend.client import config
from slamBackend.procotol.commonMessage import *
import time

class SlamClient:

    def __init__(self, serviceType, frontService):

        self.clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.clientSocket.connect((config.serverIP, config.serverPort))

        self.serviceType = serviceType

        self.frontService = frontService


    def initService(self):

        clientMessage = ClientMessage(self.serviceType, CommandType.START_SERVICE, "")

        clientMessage = clientMessage.dumpJson().encode('utf-8')

        self.clientSocket.send(clientMessage)

        res = self.clientSocket.recv(config.maxBuffSize)

        res = ServerMessage.loadJson(res.decode("utf-8"))

        if res.status != StatusType.STATUS_OK:

            e = Exception('init failed please reconnect')

            raise e


    def excuteService(self):

        self.initService()

        while(True):

            strData = self.frontService.getData()

            clientMessage = ClientMessage(self.serviceType, CommandType.RUNTIME_SERVICE, strData)

            clientMessage = clientMessage.dumpJson().encode('utf-8')

            self.clientSocket.send(clientMessage)

            res = self.clientSocket.recv(config.maxBuffSize)

            res = ServerMessage.loadJson(res.decode("utf-8"))

            if res.status != StatusType.STATUS_OK:

                e = Exception('init failed please reconnect')

                raise e

            self.frontService.callBack(res)

