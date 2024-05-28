# Overview
>KTJOCR is an Optical Character Recognition (OCR) application built using Django. It allows users to upload images or PDFs, processes them to extract text, and provides the extracted text as output.

## Features
- Image Upload: Upload images for OCR processing.
- PDF Upload: Upload PDF files for OCR processing.
- Text Extraction: Extract text from uploaded images or PDFs.
- User Authentication: Secure user authentication for accessing the application.
- Admin Interface: Manage the application through the Django admin interface.

## Requirements
- Django==5.0.6
- easyocr==1.7.1
- fitz==0.0.1.dev2
- matplotlib==3.8.4
- numpy==1.26.4
- opencv_python==4.9.0.80
- opencv_python_headless==4.9.0.80
- Pillow==10.3.0
- protobuf==4.25.3
- pytesseract==0.3.10
- Requests==2.32.2

## Installation

1. Clone the Repository
```bash
git clone https://github.com/lordethyed/ktjocr.git
cd ktjocr
```
2. Create a Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```
3. Install Dependencies
```bash
pip install -r requirements.txt
```
4. Install Tesseract OCR
- **Ubuntu:**
```bash
sudo apt-get update
sudo apt-get install tesseract-ocr
```
- **macOS:**
```bash
brew install tesseract
```
- **Windows:**
Download and install Tesseract from [here](https://github.com/UB-Mannheim/tesseract/wiki).
5. Configure Database
Modify `ktjocr/settings.py` to configure your database. By default, it uses SQLite.
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / "db.sqlite3",
    }
}
```
6. Run Migrations
```bash
python manage.py migrate
```
7. Create a Superuser
```bash
python manage.py createsuperuser
```
8. Run the Development Server
```bash
python manage.py runserver
```
Visit `http://127.0.0.1:8000/` to access the application.
