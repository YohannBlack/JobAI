from flask import Flask, request, jsonify
from flask_cors import CORS
import re
import io
import time
import logging
from typing import Dict
from concurrent.futures import ThreadPoolExecutor, as_completed
from functools import lru_cache
import pandas as pd

# === Initialisation ===
app = Flask(__name__)
CORS(app)

# === Logging ===
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

WHITESPACE_PATTERN = re.compile(r'\s+')
PUNCTUATION_PATTERN = re.compile(r'\s*([.,;:!?])\s*')
# === Classe PDFProcessor ===
class PDFProcessor:
    def __init__(self):
        self._pdf_reader = None
        self._ocr_available = None

    @property
    def pdf_reader(self):
        if self._pdf_reader is None:
            from PyPDF2 import PdfReader
            self._pdf_reader = PdfReader
        return self._pdf_reader

    @property
    def ocr_available(self):
        if self._ocr_available is None:
            try:
                import pytesseract
                from pdf2image import convert_from_bytes
                self._ocr_available = True
            except ImportError:
                self._ocr_available = False
        return self._ocr_available

    def extract_text_pypdf(self, pdf_content: bytes) -> str:
        try:
            file_obj = io.BytesIO(pdf_content)
            reader = self.pdf_reader(file_obj)
            return ' '.join([page.extract_text() or '' for page in reader.pages])
        except Exception as e:
            logger.warning(f"Erreur PyPDF2: {e}")
            return ""

    def extract_text_ocr(self, pdf_content: bytes) -> str:
        if not self.ocr_available:
            return ""
        try:
            from pdf2image import convert_from_bytes
            import pytesseract
            images = convert_from_bytes(pdf_content, dpi=150, thread_count=2)
            with ThreadPoolExecutor(max_workers=2) as ocr_executor:
                texts = list(ocr_executor.map(lambda img: pytesseract.image_to_string(img, lang='eng+fra'), images))
            return ' '.join(texts)
        except Exception as e:
            logger.error(f"Erreur OCR: {e}")
            return ""

    def extract_text(self, file) -> str:
        file.seek(0)
        pdf_content = file.read()
        # Forcer l’OCR
        return self.clean_text(self.extract_text_ocr(pdf_content))

    @staticmethod
    @lru_cache(maxsize=128)
    def clean_text(text: str) -> str:
        text = WHITESPACE_PATTERN.sub(' ', text)
        text = PUNCTUATION_PATTERN.sub(r'\1 ', text)
        return text.strip()

# === Classe InfoExtractor ===
class InfoExtractor:
    @staticmethod
    def extract_email(text):
        # Ne nettoie que les espaces parasites après le point
        text_cleaned = re.sub(r"(\.\s+)([a-zA-Z])", r".\2", text)
        match = re.search(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", text_cleaned)
        return match.group() if match else "Non trouvée"


    @staticmethod
    def extract_phone(text):
        match = re.search(r"\+?\d{1,3}[-.\s]?\d{2,3}[-.\s]?\d{2,3}[-.\s]?\d{2,3}[-.\s]?\d{2,3}", text)
        return match.group() if match else "Non trouvé"

    @staticmethod
    
    def extract_name(text):
        # Souvent le premier mot en majuscules (2 mots max) est le nom
        match = re.match(r"^([A-ZÉÈÀÇÙ][A-ZÉÈÀÇÙ]+(?:\s+[A-ZÉÈÀÇÙ][A-ZÉÈÀÇÙ]+)?)", text)
        return match.group(1) if match else "Non trouvé"

    @staticmethod
    def extract_address(text):
        match = re.search(r"\d{1,4}\s+[A-Za-z\s]+(?:St|Street|Avenue|Av|Boulevard|Blvd|Road|Rd|Rue|Chemin|Allée|Impasse),?\s+[A-Za-z\s]+", text)
        return match.group() if match else "Non trouvée"


    @staticmethod
    def extract_skills(text):
        if "COMPÉTENCES" in text:
            skills_section = text.split("COMPÉTENCES", 1)[1]
            # On coupe au mot suivant courant
            end_keywords = ["EXPÉRIENCES", "FORMATION", "RÉALISATIONS"]
            for key in end_keywords:
                if key in skills_section:
                    skills_section = skills_section.split(key)[0]
            return skills_section.strip()
        return "Non détectées"


# === Instances ===
pdf_processor = PDFProcessor()
info_extractor = InfoExtractor()

# === Fonction principale ===
def process_pdf(file) -> Dict[str, str]:
    text = pdf_processor.extract_text(file)
    if not text.strip():
        raise ValueError("Aucun texte détecté")
    tasks = {
    'nom': lambda: info_extractor.extract_name(text),
    'email': lambda: info_extractor.extract_email(text),
    'telephone': lambda: info_extractor.extract_phone(text),
    'adresse': lambda: info_extractor.extract_address(text),
    'competences': lambda: info_extractor.extract_skills(text)
    }
    results = {}
    with ThreadPoolExecutor(max_workers=3) as executor:
        futures = {executor.submit(func): key for key, func in tasks.items()}
        for future in as_completed(futures):
            key = futures[future]
            try:
                results[key] = future.result()
            except Exception as e:
                logger.error(f"Erreur extraction {key}: {e}")
                results[key] = "Erreur"
    return results

# === Route Flask ===
@app.route('/extract', methods=['POST'])
def extract():
    if 'file' not in request.files:
        return jsonify({'error': 'Aucun fichier envoyé'}), 400
    file = request.files['file']
    if not file or file.filename == '':
        return jsonify({'error': 'Aucun fichier sélectionné'}), 400

    print(f"Fichier reçu : {file.filename}") 
    try:
        start = time.time()
        result = process_pdf(file)
        logger.info(f"Extraction terminée en {time.time() - start:.2f}s")
        return jsonify(result)
    except Exception as e:
        logger.error(f"Erreur globale : {e}")
        return jsonify({'error': str(e)}), 500


@app.route("/offres", methods=["GET"])
def get_offres():
    df = pd.read_csv("./france_travail api/offres.csv")
    colonnes_voulues = ["intitule", "description", "dateCreation",  "typeContrat", "lieuTravail_libelle","origineOffre_urlOrigine"]

    # Garde uniquement ces colonnes (vérifie qu'elles existent)
    df_filtre = df[colonnes_voulues]
    return df_filtre.to_json(orient="records", force_ascii=False)


# === Lancement local ===
if __name__ == '__main__':
    app.run(debug=True, port=5000)
