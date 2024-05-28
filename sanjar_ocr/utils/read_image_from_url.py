import numpy as np
import requests
import cv2


def read_image_from_url(url):
    response = requests.get(url)
    response.raise_for_status()
    image_array = np.array(bytearray(response.content), dtype=np.uint8)
    image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
    return image
