import sys
import cv2 as cv
import ecal.core.core as ecal_core
from ecal.core.publisher import ProtoPublisher
import proto.image_pb2 as image_pb2


# Initialize eCAL input interface
ecal_core.initialize(sys.argv, "Python Protobuf Publisher")

pub = ProtoPublisher("image",
                     image_pb2.image)
protobuf_message = image_pb2.image()


cam = cv.VideoCapture(0)

while True:
    # OpenCV related
    ret_val, img = cam.read()

    # update message and image processing functions
    rows, cols, channels = img.shape
    protobuf_message.width = cols
    protobuf_message.height = rows
    protobuf_message.channels = channels
    protobuf_message.color = image_pb2.RGB
    protobuf_message.imagecompression = image_pb2.JPG
    protobuf_message.name = "logitech"
    # send image uncompressed
    # protobuf_message.data = img.tobytes()
    _, img_jpg = cv.imencode('.jpg', img)
    protobuf_message.data = img_jpg.tobytes()

    if ret_val:
        cv.imshow('my webcam', img)
        if cv.waitKey(1) == 27:
            break  # esc to quit

    # publish message
    pub.send(protobuf_message)

cv.destroyAllWindows()
