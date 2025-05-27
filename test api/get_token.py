import requests
import os
from dotenv import load_dotenv

load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")
print(client_id)
print(client_secret)

url = "https://entreprise.francetravail.fr/connexion/oauth2/access_token"
data = {
    "grant_type": "client_credentials",
    "client_id": client_id,
    "client_secret": client_secret,
    "scope": "api_offresdemploiv2 o2dsoffre"
}

response = requests.post(url, data=data)
if response.ok:
    token = response.json()["access_token"]
    print("Token récupéré ✅")
    print(token)
else:
    print("Erreur :", response.status_code)
    print(response.text)

