import cv2 as cv
import ecal.core.core as ecal_core


# Initialize eCAL input interface

cam = cv.VideoCapture(1)

while ecal_core.ok():
    # OpenCV related
    ret_val, img = cam.read()

    # update message and image processing functions

    if ret_val:
        cv.imshow('my webcam', img)
        if cv.waitKey(1) == 27:
            break  # esc to quit

    # publish message

cv.destroyAllWindows()
