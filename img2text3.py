import os
import re
from typing import List, Tuple

from google.cloud import vision
from PIL import Image, ImageDraw
import matplotlib.pyplot as plt
from matplotlib.widgets import RectangleSelector
from io import BytesIO

from ocr.documents.patterns import date_pattern, number_pattern_7_digits

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'vision_key.json'


WORD = re.compile(r"\w+")
DIGITS_PATTERN = re.compile(r"\d+")
DATE_PATTERN = re.compile(r"\b\d{2}\.\d{2}\.\d{4}\b")
CHINESE_DATE_PATTERN = re.compile(r"\b\d{4}\.\d{2}\.\d{2}\b")

# Define the regex pattern to extract 15-digit numbers
NUMBER_15_PATTERN = re.compile(r"\b\d{15}\b")  # 650400332616094

LONG_INTEGER_PATTERN = re.compile(r"\b\d{11,}\b")

# Define the regex pattern to extract vehicle IDs (alphanumeric sequences)
VEHICLE_ID_PATTERN = re.compile(r"\b[A-Z0-9]+\b")


# Define a list to store the bounding box coordinates


# Bounding box 1: (177, 251, 420, 340)
# Bounding box 2: (956, 238, 1102, 329)


def detect_text(image, google_vision_client):
    """ Detects text in an image"""

    image = vision.Image(content=image)
    response = google_vision_client.text_detection(image=image)
    if response.error.message:
        raise Exception(
            "{}\nFor more info on error messages, check: "
            "https://cloud.google.com/apis/design/errors".format(response.error.message)
        )
    else:
        texts = response.text_annotations
        ocr_text = []

        for text in texts:
            ocr_text.append(f"\r\n{text.description}")

    return texts, ocr_text


def scan_google_ocr(img_path: str,
                    regex_pattern: None,
                    bounding_box: Tuple[int, int, int, int] = None,
                    ):
    client = vision.ImageAnnotatorClient()
    image = Image.open(img_path)

    if bounding_box is not None:
        image = image.crop(bounding_box)

    # ------------------------------------------------
    # google vision only knows how to read image from file
    # following 3 lines is a quick hack to make proper input image dtype for google client
    buffer = BytesIO()
    image.save(buffer, format="PNG")
    buffer_img = buffer.getvalue()

    texts, ocr_text = detect_text(buffer_img, client)
    out_data = []
    if regex_pattern is not None:
        # out_data = regex_pattern.findall(ocr_text[0])[0]
        out_data = regex_pattern.findall(ocr_text[0])

    return texts, ocr_text, out_data, image


def main():
    # params_dict = dict(
    #     doc_path="dataset/page_1.png",
    #     doc_params=[
    #         dict(bb=(179, 253, 413, 331),
    #              regex_pattern=DATE_PATTERN),  # date pattern
    #         dict(bb=(914, 243, 1110, 336),
    #              regex_pattern=DIGITS_PATTERN),  # 7 digits Number box
    #     ],
    #
    # )

    params_dict = dict(
        doc_path="dataset/certificate_last.png",
        doc_params=[
            dict(
                bb=(770, 1445, 1179, 1516),
                regex_pattern=WORD),

            dict(
                bb=(935, 1245, 1091, 1315),
                regex_pattern=DATE_PATTERN),
            dict(
                bb=(739, 1505, 931, 1557),
                regex_pattern=DATE_PATTERN)
        ],

    )

    # params_dict = dict(
    #     doc_path="dataset/page_5.png",
    #     doc_params=[
    #         dict(
    #             bb=(64, 78, 1620, 594),
    #             regex_pattern=None),
    #
    #         # dict(
    #         #     bb=(606, 924, 999, 994),
    #         #     regex_pattern=CHINESE_DATE_PATTERN),
    #     ],
    #
    # )

    num_bbox = len(params_dict["doc_params"])

    for i in range(num_bbox):
        doc_path = params_dict["doc_path"]
        bb = params_dict["doc_params"][i]["bb"]
        regex_pattern = params_dict["doc_params"][i]["regex_pattern"]

        texts, ocr_text, out_data, image = scan_google_ocr(img_path=doc_path,
                                                           regex_pattern=regex_pattern,
                                                           bounding_box=bb)
        image.show()
        print('--------------------------------')
        print(f"bounding box index: {i}")
        print(f"out_data: {out_data}")
        print('--------------------------------')

    return None


if __name__ == '__main__':
    main()
