import fitz
import os
import cv2
from ocr.preprocessing.rotate_image import rotate_image


def extract_pages(pdf_path):
    try:
        doc = fitz.open(pdf_path)
        pages = []
        zoom_x = 2.0
        zoom_y = 2.0
        mat = fitz.Matrix(zoom_x, zoom_y)

        for page_num in range(doc.page_count):
            page = doc.load_page(page_num)
            pix = page.get_pixmap(matrix=mat)
            image_dir = f"media/{os.path.basename(pdf_path).split('/')[-1].split('.')[0]}/"
            os.makedirs(image_dir, exist_ok=True)
            image_path = os.path.join(image_dir, f"page_{page_num + 1}.png")

            # Save the pixmap to an image
            pix.save(image_path)

            # Read the saved image with OpenCV
            image = cv2.imread(image_path)

            # Rotate the image if needed
            rotated_image = rotate_image(image)

            # Save the rotated image
            cv2.imwrite(image_path, rotated_image)

            pages.append(image_path)
        return pages
    except Exception as e:
        print(f"An error occurred: {e}")
        return []