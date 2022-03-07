class PrintService():


    def __init__(self, message):

        self.message = message


    def run(self):

        print("printTest")

        print(self.message.data)

        res = "print Service is On"

        return res