import random
import os
import pyodbc
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

# Paramètres
N_USERS = 50
LIKES_PAR_USER = 20
DISLIKES_PAR_USER = 20
TOP_VILLES = 10
TOP_METIERS = 30

conn = get_connection()
cursor = conn.cursor()

# Récupérer les villes les plus fréquentes
cursor.execute(f"""
    SELECT TOP {TOP_VILLES} lieuTravail_libelle
    FROM francetravail
    WHERE lieuTravail_libelle IS NOT NULL
    GROUP BY lieuTravail_libelle
    ORDER BY COUNT(*) DESC
""")
villes = [row[0] for row in cursor.fetchall()]

# Récupérer les métiers les plus fréquents
cursor.execute(f"""
    SELECT TOP {TOP_METIERS} intitule
    FROM francetravail
    WHERE intitule IS NOT NULL
    GROUP BY intitule
    ORDER BY COUNT(*) DESC
""")
metiers = [row[0] for row in cursor.fetchall()]

# Créer les utilisateurs simulés
users = []
for user_id in range(1, N_USERS + 1):
    ville = random.choice(villes)
    prefs = random.sample(metiers, k=2)
    users.append({"id": user_id + 1000, "ville": ville, "prefs": prefs})

feedback_data = []

for user in users:
    # Offres correspondantes (like)
    cursor.execute(f"""
        SELECT TOP {LIKES_PAR_USER} id 
        FROM francetravail
        WHERE lieuTravail_libelle = ? 
        AND intitule IN (?, ?)
        ORDER BY NEWID()
    """, (user["ville"], user["prefs"][0], user["prefs"][1]))
    liked = cursor.fetchall()
    feedback_data.extend((user["id"], row[0], 1) for row in liked)

    # Offres aléatoires (dislike)
    cursor.execute(f"""
        SELECT TOP {DISLIKES_PAR_USER} id 
        FROM francetravail
        WHERE (lieuTravail_libelle != ? OR intitule NOT IN (?, ?))
        ORDER BY NEWID()
    """, (user["ville"], user["prefs"][0], user["prefs"][1]))
    disliked = cursor.fetchall()
    feedback_data.extend((user["id"], row[0], 0) for row in disliked)

# Insertion
cursor.executemany("""
    INSERT INTO feedback (user_id, offre_id, feedback) VALUES (?, ?, ?)
""", feedback_data)

conn.commit()
conn.close()

print(f"✅ Simulation terminée : {len(users)} utilisateurs, {len(feedback_data)} feedbacks insérés.")
