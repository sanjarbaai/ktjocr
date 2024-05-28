import json
# Authentication to Google API
import os
import math
from collections import Counter
from google.cloud import vision
import re
from ocr.documents.patterns import date_pattern, number_pattern_7_digits
from ocr.utils.extract_document_name import extract_document_name
from ocr.utils.read_image_from_url import read_image_from_url
from ocr.utils.save_image import save_image

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'vision_key.json'
WORD = re.compile(r"\w+")

not_found = 'not found'


def detect_text(content):
    """Detects text in the file."""

    client = vision.ImageAnnotatorClient()

    # with open(image_path, "rb") as image_file:
    #     content = image_file.read()

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


def doc_09029(image_path, file_name, reader):
    image_dir = f"media/{extract_document_name(str(file_name))}"
    # image_dir = 'media/CamScanner_02.05.2024_22.23_OoVDtBU_8xqFwLU'

    os.makedirs(image_dir, exist_ok=True)

    image, content = read_image_from_url(image_path)

    google_ocr_text = detect_text(content)

    result = reader.readtext(image)

    image = None

    if image is None:
        return json.dumps({
            'name': 'document #09029',
            'fields': {
                'date': not_found,
                '7_digits': not_found
            },
            'images': []
        })

    numbers = []
    dates = []

    numbers_image = []
    dates_image = []

    for detection in result:
        text = detection[1]
        matches_dates = re.findall(date_pattern, text)
        matches_number = re.findall(number_pattern_7_digits, text)

        if matches_dates:
            dates_path = save_image(image_dir, '09029_date', image, detection)
            if dates_path is not None:
                dates_image.append(dates_path)
                dates.extend(matches_dates)

        if matches_number:
            numbers_path = save_image(image_dir, '09029_number', image, detection)
            if numbers_path is not None:
                numbers_image.append(numbers_path)
                numbers.extend(matches_number)

    if len(numbers) < 1:
        numbers.append(not_found)
        numbers_image.append(not_found)

    if len(dates) < 1:
        dates.append(not_found)
        dates_image.append(not_found)

    for k in range(len(numbers)):
        while len(numbers[k]) > 7:
            numbers[k] = numbers[k][1:]

    return json.dumps({
        'name': '#09029',
        'original_image': image_path,
        'fields': [
            {
                'date': dates[0],
                'image': dates_image[0]
            },
            {
                '7 digits': numbers[0],
                'image': numbers_image[0]
            }
        ]
    })
