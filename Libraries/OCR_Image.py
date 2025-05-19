'''
Text OCR

Install Tesseract from
https://github.com/UB-Mannheim/tesseract/wiki
(is not a replacement for the Python library)
'''

import os
import pytesseract
from PIL import Image
import cv2
import numpy as np

# Set the Tesseract executable path
TESSERACT_PATH = os.environ.get("TESSERACT_SRV")
print(f"Tesseract server: {TESSERACT_PATH}")

pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH

def ocr_file(image_bytes, lang='eng'):
    print("Processing image file ")

    # Load image with OpenCV from image bytes
    image = cv2.imdecode(np.frombuffer(image_bytes, np.uint8), cv2.IMREAD_COLOR)

    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply thresholding
    _, thresh = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

    # Apply bluring
    # cv2.medianBlur(gray, 3)
    # blur = cv2.medianBlur(thresh, 3)

    # Convert back to PIL format
    processed_image = Image.fromarray(thresh)
    # processed_image = Image.fromarray(blur)

    # Save improved image (optional, for QA xheck purposes)
    # converted_file_name = os.path.splitext(source_file_name)[0] + '_converted.jpg'
    # cv2.imwrite(r"c:\Users\Eugene\Downloads\Materials\image1_2_converted.jpg", gray)

    # Perform OCR
    extracted_text = pytesseract.image_to_string(processed_image, lang=lang)
    # print("Extracted text:\n", extracted_text)
    return extracted_text

    # Save the extracted text to a file
    # with open(target_file_name, 'w', encoding='utf-8') as file:
    #     file.write(extracted_text)
    # print("Extracted Text file ", target_file_name)


# Testing the module
if __name__ == "__main__":
    with open(r"c:\Users\Eugene\Downloads\Images\image1_2.jpx", "rb") as image:
        f = image.read()
        b = bytearray(f)
        ocr_file(b)
        # print(b[0])