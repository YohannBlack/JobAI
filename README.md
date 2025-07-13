
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

| Composant     | Technologie                      |
|---------------|----------------------------------|
| Backend       | Python, Flask                    |
| Frontend      | React                            |
| Reco NLP      | TF-IDF, Cosine Similarity        |
| Reco Feedback | SVD (scikit-learn)               |
| NER           | spaCy                            |
| Base de données | SQL Server                     |
| Cloud         | Azure Blob Storage, Azure Function, Azure Machine Learning               |
| Géolocalisation | geopy, Nominatim               |

## Architecture du projet

```
JobAI/
├── az_func_offres_francetravail/
├── az_func_recommendation/
├── az_ml_ner/
├── backend/
│   └── app/
│       ├── models/
│       └── routes/
│           ├── __init__.py
│           ├── auth.py
│           ├── cv.py
│           ├── extract.py
│           ├── feedback.py
│           └── offres.py
├── services/
│   ├── __init__.py
│   ├── extract_text.py
│   ├── ner_processing.py
│   ├── profil_builder.py
│   └── recommender.py
├── utils/
│   ├── __init__.py
│   ├── db.py
│   ├── ner.py
│   ├── summarizer.py
│   └── text_processing.py
├── __init__.py
├── run.py
├── front-cv/
├── .env
├── .gitignore
├── README.md
└── requirements.txt
```

## Installation

### 1. Cloner le dépôt
```bash
git clone https://github.com/ton-compte/JobAI.git
cd JobAI
```

### 2. Créer un environnement virtuel Python
```bash
python -m venv .venv
.venv\Scripts\activate #sur Windows
source .venv/bin/activate #sur Linux/OSX
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
cd backEnd
python run.py
```

Frontend React :
```bash
cd front-cv
npm install
npm start
```

## Recommandation – Détails techniques

- **Matching sémantique** : le profil candidat est vectorisé avec TF-IDF, comparé aux offres.
- **Personnalisation** : les feedbacks (`like`/`dislike`) alimentent un modèle SVD.
- **Filtrage géographique** : seules les offres à moins de 60 km sont gardées.
- **NER + Résumé automatique** : le CV est transformé en un profil compact et pertinent.

## Perspectives d’évolution

- **Filtrage multi-critères** (contrat, salaire, secteur)
- **Traduction automatique** pour les profils multilingues
- Dashboard d’**analyse de performance du système**
- Mode **recruteur** avec remontée des profils pertinents

