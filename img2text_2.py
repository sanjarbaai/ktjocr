import os
import re
from google.cloud import vision
from PIL import Image, ImageDraw
import matplotlib.pyplot as plt

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
        print(text)
        ocr_text.append(f"\r\n{text.description}")

    if response.error.message:
        raise Exception(
            "{}\nFor more info on error messages, check: "
            "https://cloud.google.com/apis/design/errors".format(response.error.message)
        )
    return texts, ocr_text


def draw_boxes(image_path, texts):
    """Draw bounding boxes around the detected text."""
    image = Image.open(image_path)
    draw = ImageDraw.Draw(image)

    for text in texts:
        vertices = [(vertex.x, vertex.y) for vertex in text.bounding_poly.vertices]
        draw.line(vertices + [vertices[0]], width=2, fill='red')

    return image


def visualize_image(image_path, texts):
    """Visualize the image with bounding boxes around detected text."""
    image = draw_boxes(image_path, texts)
    plt.figure(figsize=(10, 10))
    plt.imshow(image)
    plt.axis('off')  # Hide the axis
    plt.show()


def main():
    img_path = "dataset/page_1.png"
    texts, ocr_text = detect_text(img_path)
    print(ocr_text)

    visualize_image(img_path, texts)

    print('')


if __name__ == '__main__':
    main()
