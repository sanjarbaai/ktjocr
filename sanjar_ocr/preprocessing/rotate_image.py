import pytesseract
import re
import cv2


def rotate_image(image):
    img = image
    osd = pytesseract.image_to_osd(img)
    angle = int(re.search(r'(?<=Rotate: )\d+', osd).group(0))
    if angle == 90:
        img = cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)
    elif angle == 180:
        img = cv2.rotate(image, cv2.ROTATE_180)
    elif angle == 270:
        img = cv2.rotate(image, cv2.ROTATE_90_COUNTERCLOCKWISE)
    return img
