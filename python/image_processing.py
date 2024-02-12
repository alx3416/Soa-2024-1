import cv2 as cv
import numpy as np
import lz4.frame


def encodeImage(image, compression):
    if compression == "UNCOMPRESSED":
        return image.tobytes()
    elif compression == "JPG":
        _, img_jpg = cv.imencode('.jpg', image)
        return img_jpg.tobytes()
    elif compression == "LZ4":
        return lz4.frame.compress(image.data.tobytes())


def decodeImage(imageData, shape, compression):
    imageSerialized = np.frombuffer(imageData, dtype=np.uint8)
    if compression == "UNCOMPRESSED":
        return np.reshape(imageSerialized, (shape[0], shape[1], shape[2]))
    elif compression == "JPG":
        return cv.imdecode(imageSerialized, cv.IMREAD_COLOR)
    elif compression == "LZ4":
        imageSerialized = lz4.frame.decompress(imageData)
        imageSerialized = np.frombuffer(imageSerialized, np.uint8)
        return np.reshape(imageSerialized, (shape[0], shape[1], shape[2]))