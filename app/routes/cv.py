from flask import Blueprint, request, jsonify
from app.utils.db import get_connection
from datetime import datetime, timedelta
from azure.storage.blob import generate_blob_sas, BlobSasPermissions
from app.config import blob_service_client, AZURE_CONTAINER_NAME
import logging

cv_bp = Blueprint("cv", __name__)
logger = logging.getLogger(__name__)


@cv_bp.route("/cv/<int:user_id>", methods=["GET"])
def get_cv_url(user_id):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT blob_filename FROM user_profiles WHERE user_id = ?", (user_id,))
        result = cursor.fetchone()
        conn.close()

        if not result:
            return jsonify({"error": "Aucun CV trouvé pour cet utilisateur"}), 404

        blob_filename = result[0]
        sas_token = generate_blob_sas(
            account_name=blob_service_client.account_name,
            container_name=AZURE_CONTAINER_NAME,
            blob_name=blob_filename,
            account_key=blob_service_client.credential.account_key,
            permission=BlobSasPermissions(read=True),
            expiry=datetime.utcnow() + timedelta(minutes=15)
        )
        blob_url = (
            f"https://{blob_service_client.account_name}.blob.core.windows.net/"
            f"{AZURE_CONTAINER_NAME}/{blob_filename}?{sas_token}"
        )
        return jsonify({"url": blob_url})

    except Exception as e:
        logger.error(f"[CV ERROR] {e}")
        return jsonify({"error": str(e)}), 500


@cv_bp.route("/historique_likes", methods=["GET"])
def historique_likes():
    user_id = request.args.get("user_id")
    if not user_id:
        return jsonify({"error": "user_id requis"}), 400

    try:
        conn = get_connection()
        cursor = conn.cursor()

        # Récupérer les IDs d'offres likées
        cursor.execute("""
            SELECT offre_id FROM feedback WHERE user_id = ? AND feedback = 1
        """, (user_id,))
        liked_ids = [row[0] for row in cursor.fetchall()]

        if not liked_ids:
            return jsonify([])

        placeholders = ",".join("?" for _ in liked_ids)
        query = f"""
            SELECT id AS offre_id, intitule, lieuTravail_libelle, origineOffre_urlOrigine
            FROM francetravail
            WHERE id IN ({placeholders})
        """
        cursor.execute(query, liked_ids)
        rows = cursor.fetchall()

        offres = [{
            "offre_id": row[0],
            "intitule": row[1],
            "lieuTravail_libelle": row[2],
            "origineOffre_urlOrigine": row[3]
        } for row in rows]

        conn.close()
        return jsonify(offres)

    except Exception as e:
        logger.error(f"[Historique Likes ERROR] {e}")
        return jsonify({"error": str(e)}), 500
