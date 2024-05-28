import cv2


def draw_bounding_box(image, detection, gap=50):
    bbox = detection[0]
    text = detection[1]
    score = detection[2]

    cv2.rectangle(image, tuple(map(int, bbox[0])), tuple(map(int, bbox[2])), (0, 255, 0), 5)
    x1, y1 = map(int, bbox[0])
    x2, y2 = map(int, bbox[2])
    x1 = max(0, x1 - gap)
    y1 = max(0, y1 - gap)
    x2 = min(image.shape[1], x2 + gap)
    y2 = min(image.shape[0], y2 + gap)
    cropped_image = image[y1:y2, x1:x2]

    return cropped_image
