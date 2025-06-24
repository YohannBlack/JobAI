# === Standard Libraries ===
import os
import re
import io
import uuid
import logging
import hashlib
from datetime import datetime
from typing import Dict
from concurrent.futures import ThreadPoolExecutor, as_completed
from functools import lru_cache

# === Third-party Libraries ===
import pandas as pd
import pyodbc
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from azure.storage.blob import BlobServiceClient

# === Internal Modules ===
from france_travail_api.get_token import get_access_token  # (si inutilisé, tu peux aussi le supprimer)

# === Load environment variables ===
load_dotenv()

AZURE_CONNECTION_STRING = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
AZURE_CONTAINER_NAME = os.getenv("AZURE_CONTAINER_NAME")
blob_service_client = BlobServiceClient.from_connection_string(AZURE_CONNECTION_STRING)
container_client = blob_service_client.get_container_client(AZURE_CONTAINER_NAME)

def get_connection():
    connection_string = (
        f"DRIVER={{{os.getenv('SQL_DRIVER')}}};"
        f"SERVER={os.getenv('SQL_SERVER')};"
        f"DATABASE={os.getenv('SQL_DATABASE')};"
        f"UID={os.getenv('SQL_USERNAME')};"
        f"PWD={os.getenv('SQL_PASSWORD')};"
        f"Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;"
    )
    return pyodbc.connect(connection_string)

# === Initialisation Flask ===
app = Flask(__name__)
CORS(app)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# === Traitement PDF (OCR uniquement) ===
WHITESPACE_PATTERN = re.compile(r'\s+')
PUNCTUATION_PATTERN = re.compile(r'\s*([.,;:!?])\s*')

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
        return self.clean_text(self.extract_text_ocr(pdf_content))

    @staticmethod
    @lru_cache(maxsize=128)
    def clean_text(text: str) -> str:
        text = WHITESPACE_PATTERN.sub(' ', text)
        text = PUNCTUATION_PATTERN.sub(r'\1 ', text)
        return text.strip()

pdf_processor = PDFProcessor()

# === Traitement PDF route ===
def process_pdf(file) -> Dict[str, str]:
    text = pdf_processor.extract_text(file)
    if not text.strip():
        raise ValueError("Aucun texte détecté")
    return {"texte_brut": text[:1000]}  # exemple simple, renvoie les 1000 premiers caractères

# === API ROUTES ===

@app.route('/extract', methods=['POST'])
def extract():
    if 'file' not in request.files:
        return jsonify({'error': 'Aucun fichier envoyé'}), 400
    file = request.files['file']
    if not file or file.filename == '':
        return jsonify({'error': 'Aucun fichier sélectionné'}), 400

    try:
        timestamp = datetime.utcnow().strftime('%Y%m%d%H%M%S')
        unique_id = uuid.uuid4().hex
        extension = os.path.splitext(file.filename)[1]
        blob_filename = f"{timestamp}_{unique_id}{extension}"

        file.seek(0)
        container_client.upload_blob(name=blob_filename, data=file, overwrite=True)

        file.seek(0)
        result = process_pdf(file)

        return jsonify({
            "blob_filename": blob_filename,
            "extraction": result
        })

    except Exception as e:
        logger.error(f"Erreur globale : {e}")
        return jsonify({'error': str(e)}), 500

@app.route("/offres", methods=["GET"])
def get_offres():
    df = pd.read_csv("france_travail_api/offres.csv")
    colonnes_voulues = ["intitule", "description", "dateCreation",  "typeContrat", "lieuTravail_libelle", "origineOffre_urlOrigine"]
    df_filtre = df[colonnes_voulues]
    return df_filtre.to_json(orient="records", force_ascii=False)

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='users' AND xtype='U')
        CREATE TABLE users (
            id INT IDENTITY(1,1) PRIMARY KEY,
            prenom NVARCHAR(100),
            nom NVARCHAR(100),
            email NVARCHAR(255) UNIQUE,
            password NVARCHAR(255)
        )
    ''')
    conn.commit()
    conn.close()

init_db()

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    prenom = data.get('prenom')
    nom = data.get('nom')
    email = data.get('email')
    password = hash_password(data.get('password'))

    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (prenom, nom, email, password) VALUES (?, ?, ?, ?)",
                       (prenom, nom, email, password))
        conn.commit()
        return jsonify({"message": "Compte créé avec succès"}), 201
    except pyodbc.IntegrityError:
        return jsonify({"error": "Email déjà utilisé"}), 400
    finally:
        conn.close()

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = hash_password(data.get('password'))

    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT prenom, nom FROM users WHERE email = ? AND password = ?", (email, password))
        user = cursor.fetchone()
    except Exception as e:
        return jsonify({"error": f"Erreur base de données : {str(e)}"}), 500
    finally:
        conn.close()

    if user:
        return jsonify({
            "message": "Connexion réussie",
            "user": {
                "prenom": user[0],
                "nom": user[1],
                "email": email
            }
        })
    else:
        return jsonify({"error": "Email ou mot de passe invalide"}), 401

# === Run App ===
if __name__ == '__main__':
    app.run(debug=True, port=5000)
