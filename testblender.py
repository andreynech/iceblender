import sys
sys.path.append("/usr/local/Ice-3.5.0/python")
sys.path.append("/home/andreynech/projects/veter/blender")

import bpy, threading, time

import traceback, Ice
Ice.loadSlice('Hello.ice')
Ice.updateModules()
import Demo


class HelloI(Demo.Hello):

    def __init__(self, obj, data, scene):
      Demo.Hello.__init__(self)
      self.obj = obj
      self.data = data
      self.scene = scene

    def setLocation(self, x, y, z, current=None):
        self.obj.location[0] = x
        self.obj.location[1] = y
        self.obj.location[2] = z
        self.scene.update()

    def shutdown(self, current=None):
        current.adapter.getCommunicator().shutdown()


class ServerThread(threading.Thread):

    def __init__(self, obj, data, scene):
      threading.Thread.__init__(self)
      self.obj = obj
      self.data = data
      self.scene = scene

    def run(self):
      ic = None
      try:
          props = Ice.createProperties()
          props.load('server.config')
          initdata = Ice.InitializationData()
          initdata.properties = props
          communicator = Ice.initialize(sys.argv, initdata)
          adapter = communicator.createObjectAdapter("Hello")
          object = HelloI(self.obj, self.data, self.scene)
          adapter.add(object, communicator.stringToIdentity("hello"))
          adapter.activate()
          communicator.waitForShutdown()
      except:
          traceback.print_exc()
      
      if ic:
          # Clean up
          try:
              communicator.destroy()
          except:
              traceback.print_exc()
  

# Script execution starts here
C = bpy.context
D = bpy.data
t = ServerThread(C.object, D, C.scene)
t.start()
# Here we are leaving the main thread but ServerThread is still
# running in background
