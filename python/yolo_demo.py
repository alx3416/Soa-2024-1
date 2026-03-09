import cv2 as cv
from ultralytics import YOLO

# Load the model
yolo = YOLO('yolov8n-seg.pt')

cam = cv.VideoCapture(1)
while True:
    ret_val, frame = cam.read()
    if ret_val:
        results = yolo(frame, verbose=False)
        for result in results:
            frame = result.plot()

        # show the image
        cv.imshow('frame', frame)
        # ESC to break
        if cv.waitKey(1) == 27:
            break

cv.destroyAllWindows()
