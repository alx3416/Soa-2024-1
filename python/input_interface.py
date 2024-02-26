import sys
import cv2 as cv
import numpy as np
import ecal.core.core as ecal_core
from ecal.core.subscriber import ProtoSubscriber
import ecal_interfaces as ecalio
import image_pb2

# Inicializar eCAL input interface
publisher = ecalio.ImageOutput("image")
sub = ProtoSubscriber("image", image_pb2.image)

# cascade detector
faceDetector = cv.CascadeClassifier("haarcascade_frontalface_default.xml")
# 0 default, 1 USB webcam
cam = cv.VideoCapture(0)

while ecal_core.ok():
    is_received, protobuf_message, _ = sub.receive(1)
    if is_received:

        # Convertir los datos de la imagen del mensaje protobuf a un array de numpy de 8 bits sin signo
        img = np.frombuffer(protobuf_message.data, dtype=np.uint8)

        # Convertir la imagen a escala de grises
        img_gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

        # Detectar caras 
        faces = faceDetector.detectMultiScale(img_gray, 1.1, 4)

        # Actualizar el mensaje 
        publisher.updateFaceDetected(faces)

        # Dibujar rectángulo por rostro detectado
        for (x, y, w, h) in faces:
            cv.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)

        # actualizar mensaje y procesar funciones
        publisher.updateMessage(img, "JPG")

        # enviar imagen
        publisher.send()

        cv.imshow('my webcam', img)
        if cv.waitKey(1) == 27:
            break  # salir con esc

cv.destroyAllWindows()
ecal_core.finalize()
