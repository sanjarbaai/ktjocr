import json
import os
import re


from ocr.documents.patterns import date_pattern, package_list_pattern, \
    number_of_contact_pattern, terms_of_delivery_pattern
from ocr.utils.extract_document_name import extract_document_name
from ocr.utils.read_image_from_url import read_image_from_url
from ocr.utils.save_image import save_image

not_found = 'not found'


def doc_04021(image_path, file_name, reader):
    image_dir = f"media/{extract_document_name(str(file_name))}"
    os.makedirs(image_dir, exist_ok=True)

    image = read_image_from_url(image_path)

    if image is None:
        return json.dumps({
            'name': 'document #04021',
            'fields': {
                'date': not_found,
                'date_contract': not_found,
                'packages_lists': not_found,
                'numbers_of_contacts': not_found,
                'terms_of_deliveries': not_found,
            },
            'images': []
        })

    packages_lists_image = []
    dates_image = []
    numbers_of_contacts_image = []
    terms_of_deliveries_image = []

    packages_lists = []
    dates = []
    numbers_of_contacts = []
    terms_of_deliveries = []

    result = reader.readtext(image_path)

    for detection in result:
        text = detection[1]
        matches_packages_lists = re.findall(package_list_pattern, text)
        matches_dates = re.findall(date_pattern, text)
        matches_numbers_of_contacts = re.findall(number_of_contact_pattern, text)
        matches_terms_of_deliveries = re.findall(terms_of_delivery_pattern, text)

        if matches_packages_lists:
            packages_list_path = save_image(image_dir,'04021_packages_lists', image, detection)
            if packages_list_path is not None:
                packages_lists_image.append(packages_list_path)
                packages_lists.extend(matches_packages_lists)

        if matches_dates:
            dates_path = save_image(image_dir, '04021_date', image, detection)
            if dates_path is not None:
                dates_image.append(dates_path)
                dates.extend(matches_dates)

        if matches_numbers_of_contacts:
            numbers_of_contacts_path = save_image(image_dir, '04021_numbers_of_contacts', image, detection)
            if numbers_of_contacts_path is not None:
                numbers_of_contacts_image.append(numbers_of_contacts_path)
                numbers_of_contacts.extend(matches_numbers_of_contacts)

        if matches_terms_of_deliveries:
            terms_of_deliveries_path = save_image(image_dir, '04021_terms_of_deliveries', image, detection)
            if terms_of_deliveries_path is not None:
                terms_of_deliveries_image.append(terms_of_deliveries_path)
                terms_of_deliveries.extend(matches_terms_of_deliveries)

    if len(packages_lists) < 1:
        packages_lists.append(not_found)

        packages_lists_image.append(not_found)

    if len(dates) < 2:
        dates.append(not_found)
        dates.append(not_found)

        dates_image.append(not_found)
        dates_image.append(not_found)

    if len(numbers_of_contacts) < 1:
        numbers_of_contacts.append(not_found)

        numbers_of_contacts_image.append(not_found)

    if len(terms_of_deliveries) < 1:
        terms_of_deliveries.append(not_found)

        terms_of_deliveries_image.append(not_found)

    return json.dumps({
        'name': '#04021',
        'original_image': image_path,
        'fields': [
            {
                'date': dates[0],
                'image': dates_image[0]
            },
            {
                'date contract': dates[1],
                'image': dates_image[1]
            },
            {
                'packages lists': packages_lists[0],
                'image': packages_lists_image[0]
            },
            {
                'numbers of contacts': numbers_of_contacts[0],
                'image': numbers_of_contacts_image[0]
            },
            {
                'terms of deliveries': terms_of_deliveries[0],
                'image': terms_of_deliveries_image[0]
            },
        ]
    })
