from flask import Blueprint, request, jsonify
from app.utils.db import get_connection
from app.utils.text_processing import preprocess_text, clean_entities, extract_emails, extract_phones
from app.utils.ner import ner_pipeline
from app.utils.summarizer import generate_profile_summary
from app.services.extract_text import extract_text_from_pdf
from app.services.profil_builder import profil_to_text, construire_profil
import tempfile, uuid, os
from datetime import datetime
from app.config import container_client
import logging
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

offres_bp = Blueprint("offres", __name__)

@offres_bp.route("/offres", methods=["GET"])
def get_offres():
    try:
        user_id = request.args.get("user_id")
        print(f"[DEBUG] Paramètre user_id reçu : {user_id}")
        if not user_id:
            print("[DEBUG] Aucun user_id fourni")
            return jsonify({'error': 'Paramètre user_id requis'}), 400

        conn = get_connection()
        cursor = conn.cursor()

        # Vérifie que l'utilisateur existe
        cursor.execute("SELECT id FROM users WHERE id = ?", (user_id,))
        user_row = cursor.fetchone()
        print(f"[DEBUG] Résultat SELECT user : {user_row}")
        if not user_row:
            conn.close()
            print("[DEBUG] Utilisateur non trouvé en base")
            return jsonify({'error': 'Utilisateur non trouvé'}), 404

        # Récupérer le dernier profil
        cursor.execute("""
            SELECT TOP 1 job, skill, loc
            FROM user_profiles
            WHERE user_id = ?
            ORDER BY created_at DESC
        """, (user_id,))
        profile_row = cursor.fetchone()
        print(f"[DEBUG] Dernier profil trouvé : {profile_row}")

        if not profile_row:
            conn.close()
            print("[DEBUG] Aucun profil trouvé pour cet utilisateur")
            return jsonify({'error': 'Aucun profil trouvé pour cet utilisateur'}), 404

        job, skill, loc = profile_row
        profil_text = f"{job or ''} {skill or ''} {loc or ''}"
        print(f"[DEBUG] Texte profil reconstruit : {profil_text}")

        # Récupérer les offres (dans la même connexion)
        query = """
            SELECT id, intitule, description, dateCreation, typeContrat,
                   lieuTravail_libelle, origineOffre_urlOrigine
            FROM francetravail
        """
        df = pd.read_sql(query, conn)
        conn.close()
        print(f"[DEBUG] Nombre d'offres récupérées : {len(df)}")

        df = df.dropna(subset=["intitule", "description", "lieuTravail_libelle"])
        df["texte"] = (
            df["intitule"].fillna("") + " " +
            df["description"].fillna("") + " " +
            df["lieuTravail_libelle"].fillna("")
        )

        # Vectorisation
        vectorizer = TfidfVectorizer()
        X = vectorizer.fit_transform(df["texte"].tolist() + [profil_text])
        profil_vector = X[-1]
        offres_vectors = X[:-1]
        scores = cosine_similarity(profil_vector, offres_vectors).flatten()

        df["score"] = scores
        df = df.sort_values(by="score", ascending=False)

        colonnes_avec_score = [
            "id", "intitule", "description", "dateCreation",
            "typeContrat", "lieuTravail_libelle", "origineOffre_urlOrigine", "score"
        ]
        df_filtre = df[colonnes_avec_score]

        print("[DEBUG] Offres filtrées prêtes à être renvoyées")
        return df_filtre.to_json(orient="records", force_ascii=False)

    except Exception as e:
        print(f"[ERREUR] Exception levée : {e}")
        logger.error(f"Erreur dans /offres : {e}")
        return jsonify({'error': str(e)}), 500