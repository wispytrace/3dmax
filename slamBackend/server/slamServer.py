import sys
import os
import socket

from slamBackend.services import controler
from slamBackend.server import config
from multiprocessing import Process




class SlamServer:
    
    def __init__(self):

        self.listenSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.listenSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        self.listenSocket.bind((config.serverIP, config.serverPort))

        self.listenSocket.listen(config.maxClientNum)

        self.serviceControler = controler.ServiceControler()


    def submitTask(self, connect):

        if str.find(sys.platform, "win") == -1:
            pid = os.fork()
            if pid == 0:
                return
            else:
                self.excuteTask(connect)

        process = Process(target=self.excuteTask, args=(connect,))

        process.start()


    def excuteTask(self, connect):

        while(True):

            try:
                data = connect.recv(config.maxBuffSize)

                data = data.decode("utf-8")

                if data == '':
                    raise Exception("client connect has benn closed")

                strRet = self.serviceControler.runService(data)

                connect.send(strRet.encode("utf-8"))

            except GeneratorExit as g:

                print("client has normally closed connect")
                connect.close()
                break

            except Exception as e:

                print("exceptionError:"+str(e))
                connect.close()
                break




    def close(self):
        
        self.listenSocket.close()
            







