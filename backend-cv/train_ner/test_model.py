import sys
sys.path.append('.')  
import fitz
from PIL import Image
import pytesseract
import io
import spacy

def extract_text_from_pdf(file_path):
    doc = fitz.open(file_path)
    text = ""

    for page in doc:
        page_text = page.get_text()
        if page_text.strip():
            text += page_text
        else:
            pix = page.get_pixmap(dpi=300)
            img = Image.open(io.BytesIO(pix.tobytes("png")))
            ocr_text = pytesseract.image_to_string(img, lang='fra')
            text += ocr_text

    return text
# Test avec un PDF
pdf_path = "C:/Users/dyhia/ESGI/PA2025/JobAI/backend-cv/src/ResumeS/Cette fois ci c'est la bonne.pdf"  # Remplacez par votre fichier PDF

# Extraire le texte
texte = extract_text_from_pdf(pdf_path)
print("Texte extrait:")
print(texte[:200] + "...")

# Analyser avec le modèle
nlp = spacy.load("cv_ner_model_VC_LA_BONNE")
doc = nlp(texte)

# Afficher les entités
print("\nEntités trouvées:")
for ent in doc.ents:
    print(f"{ent.label_}: {ent.text}")