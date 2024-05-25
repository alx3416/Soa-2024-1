import cv2 as cv
import ecal_interfaces as ecalio

# Initialize eCAL input interface
# publisher = ecalio.InputInterface('image')
subscriber = ecalio.ImageInput('image')
faceDetector = cv.CascadeClassifier("haarcascade_frontalface_default.xml")

while True:
    # OpenCV related
    subscriber.receive(100)
    if subscriber.messageWasReceived:
        frame = subscriber.getColorImage()
        img_gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        faces = faceDetector.detectMultiScale(img_gray, 1.1, 4)
        for (x, y, w, h) in faces:
            cv.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

        cv.imshow('my webcam', frame)
        if cv.waitKey(1) == 27:
            break  # esc to quit

cv.destroyAllWindows()

