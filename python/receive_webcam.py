import sys
import cv2 as cv
import ecal.core.core as ecal_core
import numpy as np
from ecal.core.subscriber import ProtoSubscriber
import python.image_pb2 as imagen_pb2

ecal_core.initialize(sys.argv, "Python Protobuf Subscriber")
sub = ProtoSubscriber("image", imagen_pb2.image)
protobuf_message = imagen_pb2.image()

while True:
    # OpenCV related
    ret_val, img = cam.read() 
    
ecal_core.finalize()
