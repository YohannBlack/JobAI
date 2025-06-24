import sys
sys.path.append('.')

import io
import fitz
from PIL import Image
import pytesseract
import spacy
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# --- Extraction texte PDF + OCR fallback ---
def extract_text_from_pdf(file_path):
    doc = fitz.open(file_path)
    text = ""
    for page in doc:
        page_text = page.get_text()
        if page_text.strip():
            text += page_text + "\n"
        else:
            pix = page.get_pixmap(dpi=300)
            img = Image.open(io.BytesIO(pix.tobytes("png")))
            ocr_text = pytesseract.image_to_string(img, lang='fra')
            text += ocr_text + "\n"
    return text

# --- Extraction entités avec SpaCy ---
def extract_entities(text, model_path="train_ner\cv_ner_model_VC_LA_BOO0NNE"):
    nlp = spacy.load(model_path)
    doc = nlp(text)
    entities = [(ent.label_, ent.text) for ent in doc.ents]
    return entities

# --- Étape 3 : Connexion à la base et recommandation d'offres ---
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

def recommander_offres(profil_text, top_n=10):
    try:
        conn = get_connection()
        query = """
            SELECT id, intitule, description, lieuTravail_libelle
            FROM francetravail
            WHERE intitule IS NOT NULL AND description IS NOT NULL AND lieuTravail_libelle IS NOT NULL
        """
        offres = pd.read_sql(query, conn)
        conn.close()

        # Construire un champ texte combiné pour vectorisation
        offres["texte"] = (
            offres["intitule"].fillna("") + " " +
            offres["description"].fillna("") + " " +
            offres["lieuTravail_libelle"].fillna("")
        )

        # Vectorisation TF-IDF
        vectorizer = TfidfVectorizer()
        X = vectorizer.fit_transform(offres["texte"].tolist() + [profil_text])

        profil_vector = X[-1]
        offres_vectors = X[:-1]

        # Similarité cosinus
        scores = cosine_similarity(profil_vector, offres_vectors).flatten()
        offres["score"] = scores

        # Trier et récupérer les top_n offres
        top = offres.sort_values(by="score", ascending=False).head(top_n)
        return top[["id", "intitule", "score", "lieuTravail_libelle"]]

    except Exception as e:
        print(f"Erreur dans la recommandation: {e}")
        return pd.DataFrame()

# --- Fonction principale ---
def main(pdf_path):
    print("Extraction du texte du CV...")
    texte_cv = extract_text_from_pdf(pdf_path)
    print(f"Texte extrait (extrait 200 premiers caractères):\n{texte_cv[:200]}...\n")

    print("Extraction des entités nommées avec SpaCy...")
    entities = extract_entities(texte_cv)
    print("Entités trouvées :")
    for label, text in entities:
        print(f"  - {label}: {text}")

    # --- Amélioration du profil_text ---
    labels_utiles = {"SKILL", "JOB"}
    profil_tokens = [
        text.strip()
        for label, text in entities
        if label in labels_utiles
        and len(text.strip()) > 3
        and not any(char.isdigit() for char in text)  # filtrer les nombres
    ]
    profil_text = " ".join(profil_tokens)
    
    # Fallback : si trop peu d'éléments, utiliser tout le texte
    if len(profil_text.split()) < 5:
        profil_text = texte_cv

    print("\nProfil utilisé pour la recherche :")
    print(profil_text[:300], "...\n")

    print("Recherche des offres similaires dans le CSV...")
    top_offres = recommander_offres(profil_text, top_n=10)
    if not top_offres.empty:
        print("\nTop offres recommandées :")
        print(top_offres.to_string(index=False))
    else:
        print("Aucune offre recommandée trouvée.")


if __name__ == "__main__":
    pdf_path = "C:/Users/dyhia/ESGI/PA2025/JobAI/backend-cv/src/ResumeS/CV_.pdf"
    main(pdf_path)
