import sys

import cv2 as cv
import ecal.core.core as ecal_core
from ecal.core.publisher import ProtoPublisher
import proto.image_pb2 as image_pb2

ecal_core.initialize(sys.argv, "Python Protobuf Publisher")

publisher = ProtoPublisher("image", image_pb2.imagen)

#base xd xml
face_cascade = cv.CascadeClassifier(cv.data.haarcascades + 'haarcascade_frontalface_default.xml')

cam = cv.VideoCapture(0)

while True:
    ret_val, img = cam.read()

    #-----conversion y deteccion xd-----
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=6)
    #-----------------------------------

    protobuf_message = image_pb2.imagen()
    cv.imshow('ENVIO_XD', img)

    # guardado de rostros
    facelocation_message = image_pb2.faceloation()
    for face in faces:
        facelocation_message = protobuf_message.facedetection.add()
        facelocation_message.xmin = int(face[0])
        facelocation_message.ymin = int(face[1])
        facelocation_message.xmax = int(face[0] + face[2])
        facelocation_message.ymax = int(face[1] + face[3])

    #imagen
    protobuf_message.width = img.shape[1]
    protobuf_message.height = img.shape[0]
    protobuf_message.channels = img.shape[2]
    protobuf_message.data = cv.imencode(".jpg", img)[1].tobytes()

    publisher.send(protobuf_message)

    if cv.waitKey(1) == 27:
        break

cam.release()
cv.destroyAllWindows()
