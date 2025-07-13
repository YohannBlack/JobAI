
# Job AI – Système intelligent de recommandation d’offres d’emploi

> Un moteur de recommandation intelligent basé sur le NLP, la géolocalisation et le filtrage collaboratif pour aider les candidats à trouver les offres qui leur correspondent.

## Fonctionnalités principales

- **Extraction de profil depuis un CV** (via NER + résumé automatique)
- **Filtrage géographique** (rayon 60 km autour du lieu du candidat)
- **Recommandation personnalisée** (TF-IDF + SVD)
- **Apprentissage via feedback utilisateur** (`like` / `dislike`)
- **Historique et visualisation des entités extraites**
- **Stockage cloud avec Azure Blob Storage**
- **Architecture modulaire** : Flask (backend) + React (frontend)

## Stack technique

| Composant     | Technologie                     |
|---------------|----------------------------------|
| Backend       | Python, Flask, SQLAlchemy        |
| Frontend      | React, TailwindCSS               |
| Reco NLP      | TF-IDF, Cosine Similarity        |
| Reco Feedback | SVD (scikit-learn)               |
| NER           | spaCy                            |
| Base de données | SQL Server                     |
| Cloud         | Azure Blob Storage               |
| Géolocalisation | geopy, Nominatim (OpenStreetMap) |

## Architecture du projet

```
JobAI/
│
├── app/
│   ├── routes/
│   │   ├── extract.py       # Extraction de données du CV
│   │   ├── offres.py        # Recommandation d’offres
│   │   ├── feedback.py      # Like / Dislike
│   ├── utils/
│   │   ├── ner.py           # Modèle NER
│   │   └── db.py            # Connexion à SQL Server
│   └── app.py               # Point d'entrée Flask
│
├── frontend/                # Application React (optionnel)
│
├── azure_app/               # Déploiement Azure Function (si utilisé)
│
├── requirements.txt
├── README.md
└── .env
```

## Installation

### 1. Cloner le dépôt
```bash
git clone https://github.com/ton-compte/job-ai.git
cd job-ai
```

### 2. Créer un environnement virtuel Python
```bash
python -m venv .venv
source .venv/bin/activate  # ou .venv\Scripts\activate sur Windows
```

### 3. Installer les dépendances
```bash
pip install -r requirements.txt
```

### 4. Configurer les variables d’environnement `.env`
```env
AZURE_STORAGE_CONNECTION_STRING=...
SQL_SERVER=...
SQL_DATABASE=...
SQL_USERNAME=...
SQL_PASSWORD=...
```

## Lancer l’application

```bash
flask run
```

Frontend React (si utilisé) :
```bash
cd frontend
npm install
npm run dev
```

## Recommandation – Détails techniques

- **Matching sémantique** : le profil candidat est vectorisé avec TF-IDF, comparé aux offres.
- **Personnalisation** : les feedbacks (`like`/`dislike`) alimentent un modèle SVD.
- **Filtrage géographique** : seules les offres à moins de 60 km sont gardées.
- **NER + Résumé automatique** : le CV est transformé en un profil compact et pertinent.

## Perspectives d’évolution

- Intégration d’un modèle **LightFM** ou **FAISS** pour plus de scalabilité
- **Filtrage multi-critères** (contrat, salaire, secteur)
- **Traduction automatique** pour les profils multilingues
- Dashboard d’**analyse de performance du système**
- Mode **recruteur** avec remontée des profils pertinents

