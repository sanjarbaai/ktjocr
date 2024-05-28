# Authentication to Google API
import os
import math
from collections import Counter
from google.cloud import vision
import re

from ocr.documents.patterns import date_pattern, number_pattern_7_digits

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'vision_key.json'
WORD = re.compile(r"\w+")


def detect_text(path):
    """Detects text in the file."""

    client = vision.ImageAnnotatorClient()

    with open(path, "rb") as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    # for non-dense text
    # response = client.text_detection(image=image)
    # for dense text

    response = client.document_text_detection(image=image)
    texts = response.text_annotations
    ocr_text = []

    for text in texts:
        ocr_text.append(f"\r\n{text.description}")

    if response.error.message:
        raise Exception(
            "{}\nFor more info on error messages, check: "
            "https://cloud.google.com/apis/design/errors".format(response.error.message)
        )
    return ocr_text


def main():
    img_path = "dataset/page_1.png"
    # img_path = "dataset/date_image_crop.png"
    # img_path = "dataset/7_digit_number_crop.png"
    ocr_text = detect_text(img_path)

    # matches_dates = re.findall(date_pattern, ocr_text[0])[0]

    matches_number = re.findall(number_pattern_7_digits, ocr_text[0])[0]

    print(matches_number)


if __name__ == '__main__':
    main()
