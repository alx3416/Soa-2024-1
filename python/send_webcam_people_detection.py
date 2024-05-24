import cv2 as cv
import ecal_interfaces as ecalio

# Initialize eCAL input interface
publisher = ecalio.ImageOutput("image")

cam = cv.VideoCapture(0)
hog = cv.HOGDescriptor()
hog.setSVMDetector(cv.HOGDescriptor.getDefaultPeopleDetector())

while True:
    # OpenCV related
    ret_val, img = cam.read()

    (regions, _) = hog.detectMultiScale(img,
                                        winStride=(4, 4),
                                        padding=(4, 4),
                                        scale=1.05)

    for (x, y, w, h) in regions:
        cv.rectangle(img, (x, y),
                      (x + w, y + h),
                      (0, 0, 255), 2)

    # update message and image processing functions
    publisher.updateMessage(img, "UNCOMPRESSED")

    # send image
    publisher.send()

    if ret_val:
        cv.imshow('my webcam', img)
        if cv.waitKey(1) == 27:
            break  # esc to quit

cv.destroyAllWindows()
