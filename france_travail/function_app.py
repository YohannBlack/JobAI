import os
import requests
import pyodbc
from dotenv import load_dotenv
import logging
import azure.functions as func
from get_token import get_access_token

load_dotenv()

app = func.FunctionApp()

@app.timer_trigger(schedule="0 0 4 * * *", arg_name="myTimer", run_on_startup=False, use_monitor=True)
def fetch_offres(myTimer: func.TimerRequest) -> None:
    if myTimer.past_due:
        logging.warning(" The timer is past due")

    logging.info("Début de la fonction fetch_offres")

    # Connexion base de données
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
        cursor = conn.cursor()
    except Exception as e:
        logging.error(f"Erreur connexion DB : {e}")
        return

    # Authentification API
    try:
        token = get_access_token()
    except Exception as e:
        logging.error(f"Erreur récupération token : {e}")
        cursor.close()
        conn.close()
        return

    def search_jobs(token, range_="0-149", sort="1"):
        url = "https://api.francetravail.io/partenaire/offresdemploi/v2/offres/search"
        headers = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/json"
        }
        params = {
            "range": range_,
            "sort": sort
        }

        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        return response.json()

    # Pagination et insertion
    step = 150
    max_results = 3000
    start = 0

    try:
        while start < max_results:
            end = start + step - 1
            logging.info(f"Récupération des offres {start} à {end}")
            result = search_jobs(token, range_=f"{start}-{end}")
            offres = result.get("resultats", [])

            if not offres:
                logging.info("Plus d'offres à traiter.")
                break

            for offre in offres:
                offre_id = offre.get("id", "")
                cursor.execute("SELECT 1 FROM francetravail WHERE id = ?", (offre_id,))
                if cursor.fetchone():
                    logging.info(f" Ignorée (déjà en base) : {offre_id}")
                    continue

                competences = offre.get("competences", [])
                comp_codes = ";".join([c.get("code", "") for c in competences])
                comp_libs = ";".join([c.get("libelle", "") for c in competences])
                comp_exigs = ";".join([c.get("exigence", "") for c in competences])

                partenaires = offre.get("origineOffre", {}).get("partenaires", [])
                partenaires_str = ";".join([f"{p.get('nom', '')} ({p.get('url', '')})" for p in partenaires])

                cursor.execute("""
                INSERT INTO francetravail (
                    id, intitule, description, dateCreation, dateActualisation,
                    lieuTravail_libelle, lieuTravail_latitude, lieuTravail_longitude,
                    lieuTravail_codePostal, lieuTravail_commune,
                    typeContrat, typeContratLibelle, natureContrat,
                    experienceExige, experienceLibelle,
                    competences_code, competences_libelle, competences_exigence,
                    salaire_commentaire, salaire_libelle, salaire_complement1,
                    dureeTravailLibelle, dureeTravailLibelleConverti, alternance,
                    contact_nom, contact_coordonnees1, contact_courriel,
                    urlPostulation, secteurActivite, secteurActiviteLibelle,
                    origineOffre_origine, origineOffre_urlOrigine,
                    offresManqueCandidats
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    offre_id,
                    offre.get("intitule", ""),
                    offre.get("description", "").replace('\n', ' ').replace('\r', ' '),
                    offre.get("dateCreation", ""),
                    offre.get("dateActualisation", ""),
                    offre.get("lieuTravail", {}).get("libelle", ""),
                    offre.get("lieuTravail", {}).get("latitude", None),
                    offre.get("lieuTravail", {}).get("longitude", None),
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
                    offre.get("alternance", False),
                    offre.get("contact", {}).get("nom", ""),
                    offre.get("contact", {}).get("coordonnees1", ""),
                    offre.get("contact", {}).get("courriel", ""),
                    offre.get("urlPostulation", ""),
                    offre.get("secteurActivite", ""),
                    offre.get("secteurActiviteLibelle", ""),
                    offre.get("origineOffre", {}).get("origine", ""),
                    offre.get("origineOffre", {}).get("urlOrigine", ""),
                    offre.get("offresManqueCandidats", False)
                ))

            conn.commit()
            start += step

        logging.info("Toutes les données ont été insérées avec succès.")
    except Exception as e:
        logging.error(f"Erreur durant l'insertion ou récupération : {e}")
    finally:
        cursor.close()
        conn.close()
