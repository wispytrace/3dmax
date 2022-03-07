from procotol.commonMessage import ServiceType, ClientMessage, CommandType, SlamData

from matplotlib import pyplot as  plt

from io import BytesIO

if __name__ == "__main__":




    with open("H:\\code\\3dmax\\slamBackend\\unitTest\\pic.jpg", "rb") as f:

        data = f.read()

    slamData = SlamData(data)

    print(ServiceType.PRINT_SERVICE.value)

    message = ClientMessage(ServiceType.PRINT_SERVICE, CommandType.START_SERVICE, slamData.dumpJson())

    str = message.dumpJson()

    Dict = ClientMessage.loadJson(str)

    print(Dict.type, Dict.command)

    data = Dict.data

    slamData = SlamData.loadJson(data)

    image = plt.imread(BytesIO(slamData.image), "jpg")

    print(type(image))

    plt.imsave("picshow.jpg", image)

    plt.imshow(image)

    plt.show()