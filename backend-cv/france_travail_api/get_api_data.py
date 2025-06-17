import requests
import os
import csv
from dotenv import load_dotenv
from get_token import get_access_token




#Recuperer le token



import requests

def search_jobs(range_="0-9", sort="1", mots_cles=None):
    token = get_access_token()
    url = "https://api.francetravail.io/partenaire/offresdemploi/v2/offres/search"
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json"
    }
    params = {
        "range": range_,
        "sort": sort,
    }
    # On ajoute motsCles si on veut filtrer par mot clé (à tester si accepté)
    if mots_cles:
        params["motsCles"] = mots_cles

    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    return response.json()

result = search_jobs(range_="0-50", mots_cles="pharmaceutiques")
#print(result)



import csv

def ecrire_csv(result_json, nom_fichier="offres.csv"):
    with open(nom_fichier, mode='w', newline='', encoding='utf-8-sig') as f:
        writer = csv.writer(f)

        # En-têtes du CSV
        entetes = [
            "id", "intitule", "description", "dateCreation", "dateActualisation",
            "lieuTravail_libelle", "lieuTravail_latitude", "lieuTravail_longitude",
            "lieuTravail_codePostal", "lieuTravail_commune",
            "typeContrat", "typeContratLibelle", "natureContrat",
            "experienceExige", "experienceLibelle",
            "competences_code", "competences_libelle", "competences_exigence",
            "salaire_commentaire", "salaire_libelle", "salaire_complement1",
            "dureeTravailLibelle", "dureeTravailLibelleConverti", "alternance",
            "contact_nom", "contact_coordonnees1", "contact_courriel",
            "urlPostulation", "secteurActivite", "secteurActiviteLibelle",
            "origineOffre_origine", "origineOffre_urlOrigine",
            "partenaires",  # formaté en texte
            "offresManqueCandidats"
        ]
        writer.writerow(entetes)

        for offre in result_json.get("resultats", []):
            # Gestion des compétences (peut en avoir plusieurs, on les concatène en texte)
            competences = offre.get("competences", [])
            comp_codes = ";".join([c.get("code", "") for c in competences])
            comp_libs = ";".join([c.get("libelle", "") for c in competences])
            comp_exigs = ";".join([c.get("exigence", "") for c in competences])

            # Partenaires formaté comme texte
            partenaires = offre.get("origineOffre", {}).get("partenaires", [])
            partenaires_str = ";".join([
                f"{p.get('nom', '')} ({p.get('url', '')})" for p in partenaires
            ])

            ligne = [
                offre.get("id", ""),
                offre.get("intitule", ""),
                offre.get("description", "").replace('\n', ' ').replace('\r', ' '),
                offre.get("dateCreation", ""),
                offre.get("dateActualisation", ""),
                offre.get("lieuTravail", {}).get("libelle", ""),
                offre.get("lieuTravail", {}).get("latitude", ""),
                offre.get("lieuTravail", {}).get("longitude", ""),
                offre.get("lieuTravail", {}).get("codePostal", ""),
                offre.get("lieuTravail", {}).get("commune", ""),
                offre.get("typeContrat", ""),
                offre.get("typeContratLibelle", ""),
                offre.get("natureContrat", ""),
                offre.get("experienceExige", ""),
                offre.get("experienceLibelle", ""),
                comp_codes,
                comp_libs,
                comp_exigs,
                offre.get("salaire", {}).get("commentaire", ""),
                offre.get("salaire", {}).get("libelle", ""),
                offre.get("salaire", {}).get("complement1", ""),
                offre.get("dureeTravailLibelle", ""),
                offre.get("dureeTravailLibelleConverti", ""),
                offre.get("alternance", ""),
                offre.get("contact", {}).get("nom", ""),
                offre.get("contact", {}).get("coordonnees1", ""),
                offre.get("contact", {}).get("courriel", ""),
                offre.get("urlPostulation", ""),
                offre.get("secteurActivite", ""),
                offre.get("secteurActiviteLibelle", ""),
                offre.get("origineOffre", {}).get("origine", ""),
                offre.get("origineOffre", {}).get("urlOrigine", ""),
                partenaires_str,
                offre.get("offresManqueCandidats", "")
            ]
            writer.writerow(ligne)


# write to cs
ecrire_csv(result)

