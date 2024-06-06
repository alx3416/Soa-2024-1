import cv2
from ultralytics import YOLO

# Load the model
yolo = YOLO('yolov8s-seg.pt')

# Load the video capture
videoCap = cv2.VideoCapture(0)

while True:
    ret, frame = videoCap.read()
    if ret:
        results = yolo(frame, verbose=False)
        anotated_frame = results[0].plot()

        # show the image
        cv2.imshow('frame', anotated_frame)

    # break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break

# release the video capture and destroy all windows
videoCap.release()
cv2.destroyAllWindows()
