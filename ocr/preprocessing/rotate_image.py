from copy import deepcopy

import pytesseract
import re
import cv2

# Set the Tesseract executable path
pytesseract.pytesseract.tesseract_cmd = r'/opt/homebrew/bin/tesseract'


def rotate_image(image):
    img = deepcopy(image)
    osd = pytesseract.image_to_osd(img)
    angle = int(re.search(r'(?<=Rotate: )\d+', osd).group(0))
    if angle == 90:
        img = cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)
    elif angle == 180:
        img = cv2.rotate(image, cv2.ROTATE_180)
    elif angle == 270:
        img = cv2.rotate(image, cv2.ROTATE_90_COUNTERCLOCKWISE)
    return img
