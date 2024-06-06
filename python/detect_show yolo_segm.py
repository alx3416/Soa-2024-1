from ultralytics import YOLO
import sys
import cv2 as cv
import ecal.core.core as ecal_core
import numpy as np
from ecal.core.subscriber import ProtoSubscriber
import python.image_pb2 as imagen_pb2

ecal_core.initialize(sys.argv, "Python Protobuf Subscriber")
sub = ProtoSubscriber("image", imagen_pb2.imagen)
protobuf_message = imagen_pb2

# Load the model
yolo = YOLO('yolov8s-seg.pt')

# Load the video capture
videoCap = cv.VideoCapture(0)

while True:
    ret, frame = videoCap.read()
    if ret:
        results = yolo(frame, verbose=False)
        for result in results:
            frame = result.plot()

            # show the image
        cv.imshow('frame', frame)

    # break the loop if 'q' is pressed
        if cv.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break

# release the video capture and destroy all windows
videoCap.release()
cv.destroyAllWindows()
