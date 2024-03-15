import cv2 as cv
import ecal_interfaces as ecalio

# Initialize eCAL input interface
publisher = ecalio.ImageOutput("image")

cam = cv.VideoCapture(1)

while True:
    # OpenCV related
    ret_val, img = cam.read()

    # update message and image processing functions
    publisher.updateMessage(img, "JPG")

    # send image
    publisher.send()

    if ret_val:
        cv.imshow('my webcam', img)
        if cv.waitKey(1) == 27:
            break  # esc to quit

cv.destroyAllWindows()
