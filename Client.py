import sys
sys.path.append("/usr/local/Ice-3.5.0/python")

import traceback, Ice
import math, time

Ice.loadSlice('Hello.ice')
import Demo


class Client(Ice.Application):

    def run(self, args):
        if len(args) > 1:
            print(self.appName() + ": too many arguments")
            return 1

        try:
            cube = Demo.HelloPrx.checkedCast(self.communicator().propertyToProxy('Hello.Proxy'))
            if not cube:
                print(args[0] + ": invalid proxy")
                return 1

            iterations = 100
            for i in range(0, iterations):
                y = 0
                x = math.sin(2 * math.pi / float(iterations) * i) * 5
                z = math.cos(2 * math.pi / float(iterations) * i) * 5
                cube.setLocation(x, y, z)
                time.sleep(3.0 / float(iterations)) # 3 seconds for the whole cycle

            # Comment this line if you do not want to shutdown server
            # (in blender) after this program compeletes.
            cube.shutdown()

        except Ice.Exception as ex:
            print(ex)

        return 0


app = Client()
app.main(sys.argv, "client.config")
