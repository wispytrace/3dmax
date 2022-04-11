from enum import IntEnum
import json


class ServiceType(IntEnum):

    PRINT_SERVICE = 1
    SLAM_SERVICE = 2

class CommandType(IntEnum):

    START_SERVICE = 1

    RUNTIME_SERVICE = 2

    END_SERVICE = 3

class StatusType(IntEnum):

    STATUS_OK = 1

    STATUS_CLOSE = 2

    STATUS_ERROR = -1


# image is bytes



# data is string


class ClientMessage:

    def __init__(self, type, command, data):

        self.type = type

        self.command = command

        self.data = data


    def dumpJson(self):

        jsondict = dict()

        jsondict['type'] = self.type.value

        jsondict['command'] = self.command.value

        jsondict['data'] = self.data

        jsonStr = json.dumps(jsondict)

        return jsonStr


    @staticmethod
    def loadJson(jsonStr):

        jsonDict = json.loads(jsonStr)

        serType = ServiceType(jsonDict['type'])

        command = CommandType(jsonDict['command'])

        data = jsonDict['data']

        clientMessage = ClientMessage(serType, command, data)

        return clientMessage


class ServerMessage:

    def __init__(self, type, status, data):

        self.type = type

        self.status = status

        self.data = data

    def dumpJson(self):

        jsondict = dict()

        jsondict['type'] = self.type.value

        jsondict['status'] = self.status.value

        jsondict['data'] = self.data

        jsonStr = json.dumps(jsondict)

        return jsonStr


    @staticmethod
    def loadJson(jsonStr):

        jsonDict = json.loads(jsonStr)


        serType = ServiceType(jsonDict['type'])

        status = StatusType(jsonDict['status'])

        data = jsonDict['data']

        serverMessage = ServerMessage(serType, status, data)

        return serverMessage

