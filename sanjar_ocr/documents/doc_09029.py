import json
import os
import re


from ocr.documents.patterns import date_pattern, number_pattern_7_digits
from ocr.utils.extract_document_name import extract_document_name
from ocr.utils.read_image_from_url import read_image_from_url
from ocr.utils.save_image import save_image

not_found = 'not found'


def doc_09029(image_path, file_name, reader):
    image_dir = f"media/{extract_document_name(str(file_name))}"
    os.makedirs(image_dir, exist_ok=True)

    image = read_image_from_url(image_path)

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

    result = reader.readtext(image_path)

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
