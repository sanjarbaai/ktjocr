import easyocr

from ocr.documents.doc_01207_sanitary_cn import doc_01207
from ocr.documents.doc_01707_sanitary_cn import doc_01707
from ocr.documents.doc_02016_ttn import doc_02016
from ocr.documents.doc_04021_invoice import doc_04021
from ocr.documents.doc_09015_ttn_cn import doc_09015
from ocr.documents.doc_09029_phito_kz import doc_09029

reader = easyocr.Reader(['en'], gpu=False)
reader_english_russian = easyocr.Reader(['en', 'ru'], gpu=False)
reader_chinese = easyocr.Reader(['en', 'ch_sim'], gpu=False)


def main():
    print("Hello World")


if __name__ == '__main__':
    main()
