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
        Proto = importlib.import_module(topicName + "_pb2")
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

    def updateFaceDetected(self, faces):
        del self.message.facedetection[:]
        face = 0
        for (x, y, w, h) in faces:
            self.message.facedetection.add()
            self.message.facedetection[face].xmin = x
            self.message.facedetection[face].ymin = y
            self.message.facedetection[face].xmax = x + w
            self.message.facedetection[face].ymax = y + h
            face = face + 1
            # print(self.message.facedetection[0].xmin)

