import cv2 as cv
from ultralytics import YOLO
import ecal_interfaces as ecalio

# Load the model
yolo = YOLO('yolov8s-seg.pt')

subscriber = ecalio.ImageInput('image')
detectionSubscriber = ecalio.DetectionsInput('detections')

while True:
    subscriber.receive(100)
    detectionSubscriber.receive(10)
    if subscriber.messageWasReceived:
        frame = subscriber.getColorImage()
        results = yolo(frame, verbose=False)
        for result in results:
            frame = result.plot()
        if detectionSubscriber.messageWasReceived:
            _ = detectionSubscriber.getFaceDetection()
            frame = detectionSubscriber.drawFacesDetected(frame)

        # show the image
        cv.imshow('frame', frame)
        # ESC to break
        if cv.waitKey(1) == 27:
            break
        subscriber.messageWasReceived = False
        detectionSubscriber.messageWasReceived = False

cv.destroyAllWindows()
