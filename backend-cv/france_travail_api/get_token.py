import requests
import os
from dotenv import load_dotenv

# Chargement des identifiants
load_dotenv()
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

# Récupération du token 
def get_access_token():
    url = "https://francetravail.io/connexion/oauth2/access_token?realm=%2Fpartenaire"
    data = {
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret,
        "scope": "api_offresdemploiv2 o2dsoffre"
    }
    response = requests.post(url, data=data)
    if response.ok:
        #print(response.json()["access_token"])
        return response.json()["access_token"]
    else:
        raise Exception(f"Erreur d'authentification : {response.status_code}\n{response.text}")