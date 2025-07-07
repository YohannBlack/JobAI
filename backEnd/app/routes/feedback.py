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

feedback_bp = Blueprint("/feedback", __name__)



@feedback_bp.route("/feedback", methods=["POST"])
def enregistrer_feedback():
    try:
        data = request.json
        offre_id = data.get("offre_id")
        user_id = data.get("user_id")
        feedback = data.get("feedback")

        if None in (offre_id, user_id, feedback):
            return jsonify({"error": "Champs manquants"}), 400

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT lieuTravail_libelle FROM francetravail WHERE id = ?", (offre_id,))
        ville = cursor.fetchone()
        ville = ville[0] if ville else None

        cursor.execute("""
            INSERT INTO feedback (offre_id, user_id, feedback) VALUES (?, ?, ?)
        """, (offre_id, user_id, feedback))

        if feedback == 1 and ville:
            cursor.execute("""
                SELECT poids FROM profil_ville WHERE user_id = ? AND ville = ?
            """, (user_id, ville))
            res = cursor.fetchone()
            if res:
                cursor.execute("""
                    UPDATE profil_ville SET poids = poids + 1 WHERE user_id = ? AND ville = ?
                """, (user_id, ville))
            else:
                cursor.execute("""
                    INSERT INTO profil_ville (user_id, ville, poids) VALUES (?, ?, 1)
                """, (user_id, ville))

        conn.commit()
        conn.close()
        return jsonify({"message": "Feedback enregistré avec succès"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
