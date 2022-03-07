from slamBackend.server import slamServer



if __name__ == "__main__":

    myServer = slamServer.SlamServer()

    while True:

        connect, addr = myServer.listenSocket.accept()

        myServer.submitTask(connect)


