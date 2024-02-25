import sys
import cv2 as cv
import ecal.core.core as ecal_core
import numpy as np
from ecal.core.subscriber import ProtoSubscriber
import proto.image_pb2 as imagen_pb2

ecal_core.initialize(sys.argv, "Python Protobuf Subscriber")
sub = ProtoSubscriber("image", imagen_pb2.imagen)
protobuf_message = imagen_pb2


while ecal_core.ok():
    is_received, protobuf_message, time = sub.receive(1)
    if is_received:
        img = np.frombuffer(protobuf_message.data, dtype=np.uint8)
        img = cv.imdecode(img, cv.IMREAD_COLOR)

        #carga de valores de facelocation
        faces = []
        for facelocation_message in protobuf_message.facedetection:
            xmin = facelocation_message.xmin
            ymin = facelocation_message.ymin
            xmax = facelocation_message.xmax
            ymax = facelocation_message.ymax
            faces.append((xmin, ymin, xmax, ymax))

        #dibujar rectangulos
        for (x, y, w, h) in faces:
            cv.rectangle(img, (x, y), (w, h), (255, 0, 0), 2)

        cv.imshow('RECIBIR', img)
        if cv.waitKey(1) == 27:
            break  # esc to quit
ecal_core.finalize()
