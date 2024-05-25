import cv2 as cv
import numpy as np
import lz4.frame


def encodeImage(image, compression):
    if compression == "UNCOMPRESSED":
        return image.tobytes()
    elif compression == "JPG":
        _, img_jpg = cv.imencode('.jpg', image)
        return img_jpg.tobytes()
    elif compression == "LZ4":
        return lz4.frame.compress(image.data.tobytes())


def decodeImage(imageData, shape, compression):
    imageSerialized = np.fromstring(imageData, dtype=np.uint8)
    if compression == 1:  # "UNCOMPRESSED"
        img = np.reshape(imageSerialized, (shape[0], shape[1], shape[2]))
        return img  # np.transpose(img, (1, 0, 2))
    elif compression == 2:  # "JPG"
        return cv.imdecode(imageSerialized, cv.IMREAD_COLOR)
    elif compression == 3:  # "LZ4":
        imageSerialized = lz4.frame.decompress(imageData)
        imageSerialized = np.frombuffer(imageSerialized, np.uint8)
        return np.reshape(imageSerialized, (shape[0], shape[1], shape[2]))


class FaceDetection:
    def __init__(self):
        self.detector = cv.CascadeClassifier("haarcascade_frontalface_default.xml")
        self.faces = None

    def detectFaces(self, colorFrame):
        img_gray = cv.cvtColor(colorFrame, cv.COLOR_BGR2GRAY)
        self.faces = self.detector.detectMultiScale(img_gray, 1.1, 4)

    def drawFaces(self, frame):
        for (x, y, w, h) in self.faces:
            cv.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
        self.faces = None
