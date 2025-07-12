import numpy as np
from lightfm import LightFM
from lightfm.data import Dataset
import pyodbc
import os
from dotenv import load_dotenv

load_dotenv()

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

conn = get_connection()
cursor = conn.cursor()
cursor.execute("SELECT user_id, offre_id, feedback FROM feedback")
rows = cursor.fetchall()
conn.close()

if not rows:
    print("Aucune donnée de feedback. Arrêt.")
    exit()

user_ids = set()
item_ids = set()
interactions = []

for user_id, offre_id, feedback in rows:
    user_ids.add(str(user_id))
    item_ids.add(str(offre_id))
    interactions.append((str(user_id), str(offre_id), float(feedback)))

dataset = Dataset()
dataset.fit(users=user_ids, items=item_ids)
(interactions_matrix, weights) = dataset.build_interactions(interactions)

print(f"Matrice : {interactions_matrix.shape[0]} users x {interactions_matrix.shape[1]} items")

model = LightFM(loss='warp') 
print("Début de l'entraînement manuel avec fit_partial()...")
for epoch in range(10):
    print(f"Début epoch {epoch+1}...")
    model.fit_partial(interactions_matrix, epochs=1, num_threads=1)
    print(f"Epoch {epoch+1} terminée")
    # Vérifier la perte
    loss = model.get_loss()
    print(f"Loss: {loss}")

from lightfm.evaluation import precision_at_k

precision = precision_at_k(model, interactions_matrix, k=5).mean()
print(f"🎯 Précision @5 : {precision:.3f}")
