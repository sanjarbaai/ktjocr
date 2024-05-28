import os
import cv2
from datetime import datetime
from ocr.utils.check_file_exists import check_file_exists
from ocr.utils.draw_bounding_box import draw_bounding_box


def save_image(file_dir, file_name, image, detection):
    if check_file_exists(f'{file_dir}/{file_name}.png'):
        dates_path = os.path.join(file_dir, f'{file_name}{datetime.now()}.png')
    else:
        dates_path = os.path.join(file_dir, f'{file_name}.png')
    date_image = draw_bounding_box(image, detection)

    if date_image is not None:
        cv2.imwrite(dates_path, date_image)
        return dates_path
    else:
        print(f"Error: Generated number image is empty for detection {detection}")
        return None
