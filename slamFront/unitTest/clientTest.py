import socket
from slamBackend.procotol.commonMessage import *
from slamBackend.procotol.slamDataMessage import *
def main():
    ip_port = ('127.0.0.1', 6789)

    buffer_size = 1024

    s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    s2.connect(ip_port)  # 连接服务端
    with open("/slamBackend/unitTest/pic.jpg", "rb") as f:

        data = f.read()

    slamData = SlamData(data)

    clientMessage = ClientMessage(ServiceType.PRINT_SERVICE, CommandType.START_SERVICE, slamData.dumpJson())

    clientMessage = clientMessage.dumpJson()

    s2.send(clientMessage.encode('utf-8'))

    reponse = s2.recv(buffer_size)

    print("get:", reponse.decode('utf-8'))

    reponse = ServerMessage.loadJson(reponse.decode("utf-8"))

    print(reponse.data)

    s2.close()


if __name__ == '__main__':
    main()