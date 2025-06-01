import pdfplumber
import pytesseract
from pdf2image import convert_from_path


def extract_text_from_pdf(pdf_path):
    text = ""
    
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                text += page.extract_text() or ""
        
        if text.strip():
            return text.strip()
    except Exception as e:
        print(f"Error extracting text from PDF: {e}")
        return 

def extract_text_from_image(images):
    text = ""
    try:
        for image in images:
            text_page = pytesseract.image_to_string(image)
            text += text_page + "\n"
        return text.strip()
    except Exception as e:
        print(f"Error OCR extracting text from image: {e}")
        return ""

def extract_text_from_resume(file_path):
    if file_path.lower().endswith('.pdf'):
        return extract_text_from_pdf(file_path)
    elif file_path.lower().endswith(('.png', '.jpg', '.jpeg')):
        images = convert_from_path(file_path)
        return extract_text_from_image(images)
    else:
        print("Unsupported file format. Please provide a PDF or image file.")
        return ""
