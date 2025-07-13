import os
import logging
import pyodbc
import pandas as pd
import pickle
from sklearn.decomposition import TruncatedSVD
from azure.storage.blob import BlobServiceClient
from dotenv import load_dotenv
import azure.functions as func
import numpy
import sklearn

load_dotenv()

app = func.FunctionApp()

@app.timer_trigger(schedule="0 0 4 * * *", arg_name="myTimer", run_on_startup=False, use_monitor=True)
def train_recommendation(myTimer: func.TimerRequest) -> None:
    if myTimer.past_due:
        logging.warning("The timer is past due")

    logging.info("Début de la fonction d'entraînement SVD")
    logging.info(f"Versions utilisées : numpy={numpy.__version__}, sklearn={sklearn.__version__}")
    try:
        driver = os.getenv("SQL_DRIVER")
        server = os.getenv("SQL_SERVER")
        database = os.getenv("SQL_DATABASE")
        username = os.getenv("SQL_USERNAME")
        password = os.getenv("SQL_PASSWORD")

        conn_str = (
            f"DRIVER={{{driver}}};"
            f"SERVER={server};"
            f"DATABASE={database};"
            f"UID={username};"
            f"PWD={password};"
            f"TrustServerCertificate=yes;"
        )
        conn = pyodbc.connect(conn_str)
    except Exception as e:
        logging.error(f"Erreur de connexion à la base : {e}")
        return

    try:
        query = "SELECT user_id, offre_id, feedback FROM feedback"
        feedback_df = pd.read_sql(query, conn)

        if feedback_df.empty:
            logging.warning("Aucun feedback trouvé dans la base")
            return

        logging.info("Feedbacks chargés avec succès")

        # Création de la matrice utilisateur-offre
        interaction_matrix = feedback_df.pivot_table(
            index='user_id',
            columns='offre_id',
            values='feedback',
            fill_value=0
        )

        svd = TruncatedSVD(n_components=10, random_state=42)
        svd.fit(interaction_matrix)

        logging.info("Modèle SVD entraîné avec succès")

        model_filename = "/tmp/svd_model.pkl"
        with open(model_filename, "wb") as f:
            pickle.dump(svd, f)

        # Upload dans Azure Blob Storage
        try:
            blob_conn_str = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
            container_name = os.getenv("AZURE__RECOMMANDATION_CONTAINER_NAME")

            blob_service_client = BlobServiceClient.from_connection_string(blob_conn_str)
            container_client = blob_service_client.get_container_client(container_name)

            with open(model_filename, "rb") as data:
                container_client.upload_blob(name="svd_model.pkl", data=data, overwrite=True)

            logging.info("Modèle SVD uploadé avec succès dans Azure Blob Storage")
        except Exception as e:
            logging.error(f"Erreur lors de l'upload vers Azure Blob : {e}")
    except Exception as e:
        logging.error(f"Erreur dans l'entraînement SVD : {e}")
    finally:
        conn.close()
