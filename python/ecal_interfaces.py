import sys
import importlib
import ecal.core.core as ecal_core
from ecal.core.publisher import ProtoPublisher
from ecal.core.subscriber import ProtoSubscriber
import image_processing as improc


class OutputInterface:
    def __init__(self, messageName):
        self.messageName = messageName
        self.processName = "Python_webcam_send"
        self.start()
        self.messageWasSent = False
        self.publisher = None
        self.message = self.startPublisher(self.messageName)()

    @staticmethod
    def getProto(topicName):
        Proto = importlib.import_module("proto." + topicName + "_pb2")
        return eval("Proto." + topicName)

    def startPublisher(self, topicName):
        ProtoPb = self.getProto(topicName)
        self.publisher = ProtoPublisher(topicName, ProtoPb)
        return ProtoPb

    def start(self):
        ecal_core.initialize(sys.argv, self.processName)
        ecal_core.set_process_state(1, 1, "")

    def send(self):
        self.publisher.send(self.message)
        self.messageWasSent = True

    def __del__(self):
        self.publisher.c_publisher.destroy()
        return


class ImageOutput(OutputInterface):
    def __init__(self, topicName):
        OutputInterface.__init__(self, topicName)
        return

    def updateImageProperties(self, shape):
        self.message.width = shape[0]
        self.message.height = shape[1]
        self.message.channels = shape[2]

    def updateMessage(self, image, compression):
        self.updateImageProperties(image.shape)
        self.message.data = improc.encodeImage(image, compression)

