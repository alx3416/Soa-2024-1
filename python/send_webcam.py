import cv2 as cv
import ecal_interfaces as ecalio

# Initialize eCAL input interface
publisher = ecalio.ImageOutput("image")

# cascade detector
faceDetector = cv.CascadeClassifier("haarcascade_frontalface_default.xml")
# 0 default, 1 USB webcam
cam = cv.VideoCapture(0)

while True:
    # OpenCV related
    ret_val, img = cam.read()

    # face detection
    img_gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    faces = faceDetector.detectMultiScale(img_gray, 1.1, 4)
    publisher.updateFaceDetected(faces)
    for (x, y, w, h) in faces:
        cv.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)

    # update message and image processing functions
    publisher.updateMessage(img, "JPG")

    # send image
    publisher.send()

    if ret_val:
        cv.imshow('my webcam', img)
        if cv.waitKey(1) == 27:
            break  # esc to quit

cv.destroyAllWindows()
