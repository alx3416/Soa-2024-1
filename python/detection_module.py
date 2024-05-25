import cv2 as cv
import ecal_interfaces as ecalio

# Initialize eCAL input interface
# publisher = ecalio.InputInterface('image')
subscriber = ecalio.ImageInput('image')
faceDetector = ecalio.improc.FaceDetection()

while True:
    # OpenCV related
    subscriber.receive(100)
    if subscriber.messageWasReceived:
        frame = subscriber.getColorImage()
        faceDetector.detectFaces(frame)
        faceDetector.drawFaces(frame)

        cv.imshow('my webcam', frame)
        if cv.waitKey(1) == 27:
            break  # esc to quit
        subscriber.messageWasReceived = False

cv.destroyAllWindows()

