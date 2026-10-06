import cv2
import pytesseract
import re
import os


# Tesseract OCR path
# Use the local Windows path if Tesseract is installed.
# On deployment servers, Tesseract will be found from the system PATH.

tesseract_path = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

if os.path.exists(tesseract_path):
    pytesseract.pytesseract.tesseract_cmd = tesseract_path


def clean_text(text: str):

    text = text.replace("\n", " ")

    text = re.sub(r"\s+", " ", text)

    text = text.strip()

    return text


def analyze_image(image_path: str):

    # Check that the image exists
    if not os.path.exists(image_path):

        return {
            "success": False,
            "message": "Image file was not found."
        }


    # Read image
    image = cv2.imread(image_path)


    if image is None:

        return {
            "success": False,
            "message": "Could not read the image."
        }


    # Get image information
    height, width, channels = image.shape


    # Convert image to grayscale
    gray = cv2.cvtColor(
        image,
        cv2.COLOR_BGR2GRAY
    )


    # Improve OCR readability
    gray = cv2.threshold(
        gray,
        0,
        255,
        cv2.THRESH_BINARY + cv2.THRESH_OTSU
    )[1]


    # Extract text
    text = pytesseract.image_to_string(
        gray
    )


    cleaned_text = clean_text(text)


    # No text detected
    if not cleaned_text:

        return {
            "success": False,
            "message": (
                "No readable text was detected "
                "in the screenshot."
            )
        }


    return {
        "success": True,
        "width": width,
        "height": height,
        "channels": channels,
        "text": cleaned_text,
        "message": "Image analyzed successfully."
    }