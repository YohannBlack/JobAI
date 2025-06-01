import re

import pdfplumber  # Changed from fitz
import pytesseract
from PIL import Image

from src.tools.logger import AppLogger

logger = AppLogger(
    name="TextExtractor",
    level="DEBUG",
    log_file="parser.log",
    console_level="INFO",
    file_level="DEBUG",
)


def extract_text_from_pdf(pdf_path):
    text = ""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        return text.strip()
    except Exception as e:
        logger.error(f"Error reading PDF {pdf_path} with pdfplumber: {e}")
        return None


def extract_text_from_image(image_path):
    try:
        text = pytesseract.image_to_string(Image.open(image_path))
        return text
    except Exception as e:
        logger.error(f"Error processing image {image_path} with Tesseract: {e}")
        if "TesseractNotFoundError" in str(type(e)):
            logger.error("Tesseract is not installed or not found in your PATH.")
            logger.warning("Please install Tesseract and/or set pytesseract.tesseract_cmd")
        return None

def extract_years_of_experience(text):
    if not text:
        return None

    patterns = [
        r"(\d+\.?\d*)\+?\s*years?(\s*of)?\s*(?:professional\s*)?experience",
        r"(\d+\.?\d*)\+?\s*yrs?(\s*of)?\s*(?:professional\s*)?experience",
        r"experience\s*of\s*(\d+\.?\d*)\+?\s*years?",
        r"(\d+\.?\d*)\s*years?\s*work(?:ing)?\s*experience",
    ]

    max_years = 0
    found = False

    for pattern in patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        for match in matches:
            year_str = (
                match
                if isinstance(match, str)
                else (match[0] if match[0] else match[1])
            )
            if year_str:
                try:
                    years = float(year_str)
                    if years > max_years:
                        max_years = years
                    found = True
                except ValueError:
                    continue 

    if found:
        return max_years

    return None