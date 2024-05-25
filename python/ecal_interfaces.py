import sys
import importlib
import cv2
import ecal.core.core as ecal_core
from ecal.core.publisher import ProtoPublisher
from ecal.core.subscriber import ProtoSubscriber
import numpy as np
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
        self.updateCompression(compression)

    def updateCompression(self, compression):
        if compression == "UNCOMPRESSED":
            self.message.imagecompression = 1
        elif compression == "JPG":
            self.message.imagecompression = 2
        elif compression == "LZ4":
            self.message.imagecompression = 3
        else:
            self.message.imagecompression = 0

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


class DetectionsOutput(OutputInterface):
    def __init__(self, topicName):
        OutputInterface.__init__(self, topicName)
        return

    def updateMessage(self, faces, frame):
        frameSize = frame.shape
        self.message.imagewidth = frameSize[0]
        self.message.imageheight = frameSize[1]
        self.updateFacesDetected(faces)

    def updateFacesDetected(self, facesDetected):
        del self.message.faces[:]
        face = 0
        for (x, y, w, h) in facesDetected:
            self.message.faces.add()
            self.message.faces[face].left = x
            self.message.faces[face].up = y
            self.message.faces[face].right = x + w
            self.message.faces[face].down = y + h
            face = face + 1


class InputInterface:
    def __init__(self, topicName):
        self.topicName = topicName
        self.processName = "Python_webcam_receive"
        self.start()
        self.messageWasReceived = False
        self.subscriber = None
        self.ret = int()
        self.message = self.startSubscriber(self.topicName)()

    @staticmethod
    def getProto(topicName):
        Proto = importlib.import_module(topicName + "_pb2")
        return eval("Proto." + topicName)

    def startSubscriber(self, topicName):
        ProtoPb = self.getProto(topicName)
        self.subscriber = ProtoSubscriber(topicName, ProtoPb)
        self.messageWasReceived = False
        return ProtoPb

    def start(self):
        ecal_core.initialize(sys.argv, self.processName)
        ecal_core.set_process_state(1, 1, "")

    def receive(self, waitTime):
        self.ret, self.message, timeStamp = self.subscriber.receive(waitTime)
        if self.ret != 0:
            self.messageWasReceived = True

    def waitForMessage(self, waitTime):
        self.messageWasReceived = False
        self.receive(waitTime)
        return self.messageWasReceived

    def __del__(self):
        self.subscriber.c_subscriber.destroy()
        return


class ImageInput(InputInterface):
    def __init__(self, topicName):
        InputInterface.__init__(self, topicName)
        return

    def getColorImage(self):
        if self.messageWasReceived:
            shape = [self.message.width, self.message.height, 3]
            return improc.decodeImage(self.message.data, shape, self.message.imagecompression)
        else:
            raise TypeError

    def getImageProperties(self):
        return (
            self.message.width,
            self.message.height,
            self.message.channels
        )

    def getFaceDetection(self):
        return self.message.facedetection
