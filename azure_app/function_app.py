import os
import logging
import pyodbc
import pandas as pd
import pickle
from sklearn.decomposition import TruncatedSVD
from azure.storage.blob import BlobServiceClient
import azure.functions as func
from dotenv import load_dotenv

load_dotenv()

def get_sql_connection():
    server = os.getenv("SQL_SERVER")
    database = os.getenv("SQL_DATABASE")
    username = os.getenv("SQL_USERNAME")
    password = os.getenv("SQL_PASSWORD")
    driver = os.getenv("SQL_DRIVER")

    conn_str = f'DRIVER={{{driver}}};SERVER={server};DATABASE={database};UID={username};PWD={password}'
    return pyodbc.connect(conn_str)

def main(mytimer: func.TimerRequest) -> None:
    logging.info('Starting SVD training Azure Function')

    try:
        conn = get_sql_connection()
        query = "SELECT user_id, offre_id, feedback_score FROM feedback"
        feedback_df = pd.read_sql(query, conn)
        conn.close()

        if feedback_df.empty:
            logging.warning("Aucun feedback trouvé dans la base")
            return

        interaction_matrix = feedback_df.pivot_table(
            index='user_id',
            columns='offre_id',
            values='feedback_score',
            fill_value=0
        )

        svd = TruncatedSVD(n_components=10, random_state=42)
        svd.fit(interaction_matrix)

        model_filename = "/tmp/svd_model.pkl"
        with open(model_filename, "wb") as f:
            pickle.dump(svd, f)

        conn_str = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
        container_name = os.getenv("AZURE_CONTAINER_NAME")
        blob_service_client = BlobServiceClient.from_connection_string(conn_str)
        container_client = blob_service_client.get_container_client(container_name)

        with open(model_filename, "rb") as data:
            container_client.upload_blob(name="svd_model.pkl", data=data, overwrite=True)

        logging.info("Modèle SVD entraîné et uploadé avec succès dans Azure Blob Storage")

    except Exception as e:
        logging.error(f"Erreur dans la fonction d'entraînement SVD : {e}", exc_info=True)
