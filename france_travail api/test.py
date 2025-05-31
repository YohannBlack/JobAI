import requests
import os
import csv
from dotenv import load_dotenv

load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

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
        return response.json()["access_token"]
    else:
        raise Exception(f"Erreur d'authentification : {response.status_code}\n{response.text}")

def search_jobs(token, keywords="developpeur", limit=10):
    url = "https://api.francetravail.fr/offresdemploi/v2/search"
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json"
    }
    params = {
        "motsCles": keywords,
        "range": limit,
        # Tu peux ajouter d’autres filtres si besoin, ex: "distance": 20
    }
    response = requests.get(url, headers=headers, params=params)
    if response.ok:
        return response.json()
    else:
        raise Exception(f"Erreur récupération offres : {response.status_code}\n{response.text}")

def save_jobs_to_csv(jobs, filename="offres.csv"):
    # On suppose que jobs['results'] contient la liste des offres
    results = jobs.get("results", [])

    with open(filename, mode='w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ["id", "intitule", "description", "lieuTravail", "datePublication", "typeContrat"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for job in results:
            writer.writerow({
                "id": job.get("id"),
                "intitule": job.get("intitule"),
                "description": job.get("description"),
                "lieuTravail": job.get("lieuTravail", {}).get("libelle", ""),
                "datePublication": job.get("datePublication"),
                "typeContrat": job.get("typeContrat", {}).get("libelle", "")
            })

if __name__ == "__main__":
    token = get_access_token()
    jobs = search_jobs(token, keywords="développeur", limit=10)
    save_jobs_to_csv(jobs)
    print("Fichier offres.csv créé avec succès !")
