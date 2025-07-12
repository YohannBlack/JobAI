import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.decomposition import TruncatedSVD
from geopy.distance import geodesic
from geopy.geocoders import Nominatim
from flask import Blueprint, request, jsonify
import logging
from app.utils.db import get_connection

from azure.storage.blob import BlobServiceClient
import pickle
import io

def load_svd_model_from_blob():
    conn_str = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
    container_name = os.getenv("AZURE_CONTAINER_NAME")

    blob_service_client = BlobServiceClient.from_connection_string(conn_str)
    container_client = blob_service_client.get_container_client(container_name)
    blob_client = container_client.get_blob_client("svd_model.pkl")

    stream = io.BytesIO()
    blob_data = blob_client.download_blob()
    blob_data.readinto(stream)
    stream.seek(0)
    return pickle.load(stream)



logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
offres_bp = Blueprint("offres", __name__)

@offres_bp.route("/offres", methods=["GET"])
def get_offres():
    try:
        user_id = request.args.get("user_id")
        logger.info(f"[DEBUG] Paramètre user_id reçu : {user_id}")
        if not user_id:
            return jsonify({'error': 'Paramètre user_id requis'}), 400

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT id FROM users WHERE id = ?", (user_id,))
        user_row = cursor.fetchone()
        if not user_row:
            conn.close()
            return jsonify({'error': 'Utilisateur non trouvé'}), 404

        cursor.execute("""
            SELECT TOP 1 job, skill, loc
            FROM user_profiles
            WHERE user_id = ?
            ORDER BY created_at DESC
        """, (user_id,))
        profile_row = cursor.fetchone()
        if not profile_row:
            conn.close()
            return jsonify({'error': 'Aucun profil trouvé pour cet utilisateur'}), 404

        job, skill, loc = profile_row
        profil_text = f"{job or ''} {skill or ''} {loc or ''}".strip()
        logger.info(f"[DEBUG] Texte profil reconstruit : {profil_text}")

        # Charger les feedbacks
        feedback_query = "SELECT user_id, offre_id, feedback FROM feedback"
        feedback_df = pd.read_sql(feedback_query, conn)

        # Charger les offres
        offres_query = """
            SELECT id, intitule, description, dateCreation, typeContrat,
                   lieuTravail_libelle, origineOffre_urlOrigine,
                   lieuTravail_latitude, lieuTravail_longitude
            FROM francetravail
            WHERE lieuTravail_latitude IS NOT NULL AND lieuTravail_longitude IS NOT NULL
        """
        offres_df = pd.read_sql(offres_query, conn)
        conn.close()

        if offres_df.empty:
            return jsonify([])

         ### SVD : Recommandation basée sur feedback utilisateur ###
        interaction_matrix = feedback_df.pivot_table(index='user_id', columns='offre_id', values='feedback', fill_value=0)
        user_id_int = int(user_id)

        if user_id_int not in interaction_matrix.index:
            logger.info("[DEBUG] Aucune interaction pour cet utilisateur, on continue avec le tri classique")
            interaction_reco_ids = offres_df["id"].tolist()
        else:
            try:
                svd = load_svd_model_from_blob()
                latent_matrix = svd.transform(interaction_matrix)
                predicted_scores = np.dot(latent_matrix, svd.components_)
                user_idx = interaction_matrix.index.tolist().index(user_id_int)
                user_pred = predicted_scores[user_idx]

                # Masquer les offres déjà notées
                mask = interaction_matrix.loc[user_id_int].values > 0
                user_pred[mask] = -np.inf

                top_indices = np.argsort(user_pred)[::-1]
                offre_id_map = list(interaction_matrix.columns)

                interaction_reco_ids = [
                    offre_id_map[i]
                    for i in top_indices
                    if offre_id_map[i] in offres_df["id"].astype(str).tolist()
                ]
                logger.info(f"[DEBUG] {len(interaction_reco_ids)} offres recommandées via SVD")
            except Exception as e:
                logger.error(f"[ERREUR] Chargement du modèle SVD depuis Azure Blob : {e}", exc_info=True)
                interaction_reco_ids = offres_df["id"].tolist()
        ### FIN SVD ###

        # Géocodage du profil
        geolocator = Nominatim(user_agent="job-reco-app")
        location = geolocator.geocode(loc + ", France", timeout=10) if loc else None
        if location:
            coord_cv = (location.latitude, location.longitude)
            offres_df["distance_km"] = offres_df.apply(
                lambda row: geodesic(coord_cv, (row['lieuTravail_latitude'], row['lieuTravail_longitude'])).km,
                axis=1
            )
            offres_df = offres_df[offres_df["distance_km"] <= 60]
            logger.info(f"[DEBUG] Offres après filtrage géographique : {len(offres_df)}")

        if offres_df.empty:
            return jsonify([])

        offres_df["texte"] = (
            offres_df["intitule"].fillna("") + " " +
            offres_df["description"].fillna("") + " " +
            offres_df["lieuTravail_libelle"].fillna("")
        )

        vectorizer = TfidfVectorizer()
        X = vectorizer.fit_transform(offres_df["texte"].tolist() + [profil_text])
        profil_vector = X[-1]
        offres_vectors = X[:-1]
        scores = cosine_similarity(profil_vector, offres_vectors).flatten()
        offres_df["score"] = scores

        offres_df = offres_df[offres_df["id"].isin(interaction_reco_ids)]

        offres_df = offres_df.sort_values(by="score", ascending=False)

        colonnes_finales = [
            "id", "intitule", "description", "dateCreation",
            "typeContrat", "lieuTravail_libelle", "origineOffre_urlOrigine", "score"
        ]
        return offres_df[colonnes_finales].to_json(orient="records", force_ascii=False)

    except Exception as e:
        logger.error(f"Erreur dans /offres : {e}", exc_info=True)
        return jsonify({'error': str(e)}), 500