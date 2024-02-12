import sys
import cv2 as cv
import ecal.core.core as ecal_core
import numpy as np
from ecal.core.subscriber import ProtoSubscriber
import proto.image_pb2 as imagen_pb2

ecal_core.initialize(sys.argv, "Python Protobuf Subscriber")
sub = ProtoSubscriber("mensaje imagen", imagen_pb2.imagen)
protobuf_message = imagen_pb2.imagen()

while ecal_core.ok():
    is_received, protobuf_message, time = sub.receive(1)
    if is_received:
        img = np.frombuffer(protobuf_message.data, dtype=np.uint8)
        # uncompressed
        # img = np.reshape(img, (protobuf_message.height, protobuf_message.width, protobuf_message.channels))

        # jpg
        img = cv.imdecode(img, cv.IMREAD_COLOR)

        cv.imshow('my webcam', img)
        if cv.waitKey(1) == 27:
            break  # esc to quit
ecal_core.finalize()
