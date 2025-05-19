from flask import Flask, request, jsonify
from flask_cors import CORS
import pytesseract
from pdf2image import convert_from_bytes
from PIL import Image
import re

app = Flask(__name__)
CORS(app)  # Autorise les appels depuis React

@app.route("/extract", methods=["POST"])
def extract():
    file = request.files['file']
    if not file:
        return jsonify({"error": "Aucun fichier reçu"}), 400

    # Convertir PDF en images
    images = convert_from_bytes(file.read())

    # OCR sur chaque page
    text = ''
    for img in images:
        text += pytesseract.image_to_string(img)

    # Extraction simple d'infos
    data = {
        "Nom": extract_name(text),
        "Téléphone": extract_phone(text),
        "Adresse": extract_address(text),
        "Compétences": extract_skills(text)
    }

    return jsonify(data)

def extract_name(text):
    lines = text.split('\n')
    for line in lines:
        if len(line.strip().split()) == 2:
            return line.strip()
    return "Non trouvé"

def extract_phone(text):
    match = re.search(r'\b(\d{2}[\s.-]?){5}\b', text)
    return match.group(0) if match else "Non trouvé"

def extract_address(text):
    for line in text.split('\n'):
        if "rue" in line.lower() or "avenue" in line.lower() or "bd" in line.lower():
            return line.strip()
    return "Non trouvée"

def extract_skills(text):
    keywords = ["Python", "Java", "C++", "React", "Excel", "SQL", "Machine Learning"]
    found = [k for k in keywords if k.lower() in text.lower()]
    return ", ".join(found) if found else "Non détectées"

if __name__ == "__main__":
    app.run(debug=True)
