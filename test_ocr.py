import pytesseract
from PIL import Image

# Set the Tesseract executable path
pytesseract.pytesseract.tesseract_cmd = r'/opt/homebrew/bin/tesseract'

# Path to a test image file
# image_path = 'path/to/your/test/image.png'  # Replace with the path to an actual image file
image_path = 'dataset/page_1.png'  # Replace with the path to an actual image file

# Open the image file
with Image.open(image_path) as img:
    # Use Tesseract to do OCR on the image
    text = pytesseract.image_to_string(img)
    print(text)
