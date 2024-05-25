import json
import os
import re

from ocr.documents.patterns import number_pattern_9_digits
from ocr.utils.extract_document_name import extract_document_name
from ocr.utils.read_image_from_url import read_image_from_url
from ocr.utils.save_image import save_image

not_found = 'not found'


def doc_02016(image_path, file_name, reader):
    image_dir = f"media/{extract_document_name(str(file_name))}"
    os.makedirs(image_dir, exist_ok=True)

    image = read_image_from_url(image_path)
    if image is None:
        return json.dumps({
            'name': 'document #02016',
            'fields': {
                'number': 'not found'
            },
            'images': []
        })

    numbers = []
    images = []

    result = reader.readtext(image)

    for detection in result:
        text = detection[1]
        matches_number = re.findall(number_pattern_9_digits, text)

        if matches_number:
            number_path = save_image(image_dir, '02016_number', image, detection)
            if number_path is not None:
                images.append(number_path)
                numbers.extend(matches_number)

    if len(numbers) < 1:
        numbers.append(not_found)
        images.append(not_found)

    return json.dumps({
        'name': '#02016',
        'original_image': image_path,
        'fields': [
            {
                'number': numbers[0],
                'image': images[0]
            },
        ]
    })