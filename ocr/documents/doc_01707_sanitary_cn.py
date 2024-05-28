import json
import os
import re

from ocr.documents.patterns import number_pattern_15_digits, date_pattern
from ocr.utils.extract_document_name import extract_document_name
from ocr.utils.read_image_from_url import read_image_from_url
from ocr.utils.save_image import save_image

not_found = 'not found'


def doc_01707(image_path, file_name, reader):
    image_dir = f"media/{extract_document_name(str(file_name))}"
    os.makedirs(image_dir, exist_ok=True)

    image = read_image_from_url(image_path)

    if image is None:
        return json.dumps({
            'name': 'document #07207',
            'fields': {
                'number': not_found
            },
            'images': []
        })

    dates = []
    numbers = []

    dates_image = []

    numbers_image = []

    result = reader.readtext(image_path)

    for detection in result:
        text = detection[1]

        matches_dates = re.findall(date_pattern, text)
        matches_number = re.findall(number_pattern_15_digits, text)

        if matches_number:
            number_path = save_image(image_dir, '01707_number', image, detection)
            if number_path is not None:
                numbers_image.append(number_path)
                numbers.extend(matches_number)

        if matches_dates:
            print(matches_dates)
            dates_path = save_image(image_dir, '01707_date', image, detection)
            if dates_path is not None:
                dates_image.append(dates_path)
                dates.extend(matches_dates)

    if len(numbers) < 1:
        numbers.append(not_found)
        numbers_image.append(not_found)

    if len(dates) < 1:
        dates.append(not_found)
        dates_image.append(not_found)

    return json.dumps({
        'name': '#01707',
        'original_image': image_path,
        'fields': [
            {
                'number': numbers[0],
                'image': numbers_image[0]
            },
            {
                'date': dates[0],
                'image': dates_image[0]
            },
        ]
    })
