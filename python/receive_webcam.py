import cv2 as cv
import ecal_interfaces as ecalio  # Assuming the classes are in ecal_interfaces.py


# Instantiate the ImageInput class
image_input = ecalio.ImageInput("image")

while True:
    print(len(str(image_input.getFaceDetection())))

    img = image_input.receive_data()
    if img is not None:
        # Display the image
        cv.imshow('my webcam', img)
        if cv.waitKey(1) == 27:
            break  # esc to quit 

