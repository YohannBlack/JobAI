from flask import Blueprint, request, jsonify
from app.utils.db import get_connection
from app.utils.text_processing import preprocess_text, extract_emails, extract_phones
from app.utils.ner import ner_pipeline
from app.utils.summarizer import generate_profile_summary
from app.services.extract_text import extract_text_from_pdf
from app.services.profil_builder import profil_to_text, construire_profil
from app.config import container_client
import tempfile, uuid, os
from datetime import datetime
import re

extract_bp = Blueprint("extract", __name__)

@extract_bp.route('/extract', methods=['POST'])
def extract():
    if 'file' not in request.files:
        return jsonify({'error': 'Aucun fichier envoyé'}), 400
    file = request.files['file']
    if not file or file.filename == '':
        return jsonify({'error': 'Aucun fichier sélectionné'}), 400

    try:
        # Enregistrement dans Azure
        timestamp = datetime.utcnow().strftime('%Y%m%d%H%M%S')
        unique_id = uuid.uuid4().hex
        extension = os.path.splitext(file.filename)[1]
        blob_filename = f"{timestamp}_{unique_id}{extension}"
        file.seek(0)
        container_client.upload_blob(name=blob_filename, data=file, overwrite=True)

        # Lecture fichier temporaire
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            file.seek(0)
            tmp.write(file.read())
            tmp_path = tmp.name

        # Extraction et NER
        result = extract_text_from_pdf(tmp_path)
        result_preprocess = preprocess_text(result)
        ner_results = ner_pipeline(result_preprocess)

        df_entities = [(ent['entity_group'], ent['word']) for ent in ner_results]
        emails = extract_emails(result_preprocess)
        phones = extract_phones(result_preprocess)

        df_entities += [('EMAIL', email) for email in emails]
        df_entities += [('PHONE', phone) for phone in phones]

        profil = construire_profil(df_entities)
        profil_text = profil_to_text(profil)
        profil_summary = generate_profile_summary(profil_text)

        entities_list = [{"label": label, "text": text} for (label, text) in df_entities]
        email = next((text for label, text in df_entities if label == "EMAIL"), None)
        ville = next((text for label, text in df_entities if label == "LOC"), None)
        job = next((text for label, text in df_entities if label == "JOB"), None)
        skills = [text for label, text in df_entities if label in ["SKILL", "MISC"]]
        skills_text = ", ".join(set(skills)) if skills else None

        if email:
            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute("SELECT id FROM users WHERE email = ?", (email,))
            user_row = cursor.fetchone()

            if user_row:
                user_id = user_row[0]
                cursor.execute("""
                    INSERT INTO user_profiles (user_id, job, skill, loc, blob_filename)
                    VALUES (?, ?, ?, ?, ?)
                """, (user_id, job, skills_text, ville, blob_filename))
                conn.commit()
            else:
                print(f"Aucun utilisateur trouvé avec l’email {email}")

            conn.close()

        return jsonify({
            "blob_filename": blob_filename,
            "extraction": profil_text,
            "entities": entities_list
        })

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'error': f"Une erreur est survenue : {str(e)}"}), 500



def is_ville_valide(loc):
    loc = loc.lower()
    exclusions = ['rue', 'avenue', 'boulevard', 'place', 'impasse', 'chemin', 'quai']
    if any(x in loc for x in exclusions):
        return False

    return bool(re.match(r"^[a-zA-Zàâäéèêëîïôöùûüç' \-]{2,}$", loc))

@extract_bp.route('/update-profile', methods=['POST'])
def update_profile():
    try:
        data = request.get_json()
        print("📥 Données reçues depuis le front :", data)

        entities = data.get("entities", [])
        blob_filename = data.get("blob_filename", None)

        if not blob_filename or not entities:
            return jsonify({"error": "Données manquantes"}), 400

        # Extraction des entités
        locs = [e["text"] for e in entities if e["label"] == "LOC"]
        emails = [e["text"] for e in entities if e["label"] == "EMAIL"]
        phones = [e["text"] for e in entities if e["label"] == "PHONE"]
        jobs = [e["text"] for e in entities if e["label"] == "JOB"]
        skills = [e["text"] for e in entities if e["label"] in ["SKILL", "MISC"]]

        ville_candidates = [loc for loc in locs if is_ville_valide(loc)]
        ville = ville_candidates[0] if ville_candidates else None
        email = emails[0] if emails else None
        phone = phones[0] if phones else None
        job = jobs[0] if jobs else None
        skills_text = ", ".join(set(skills)) if skills else None

        if not email:
            return jsonify({"error": "Email manquant pour identifier l'utilisateur"}), 400

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT id FROM users WHERE email = ?", (email,))
        user_row = cursor.fetchone()

        if user_row:
            user_id = user_row[0]
        else:
            cursor.execute("INSERT INTO users (email, phone) VALUES (?, ?)", (email, phone))
            user_id = cursor.lastrowid
            print("👤 Nouvel utilisateur inséré avec ID :", user_id)

        cursor.execute("""
            SELECT TOP 1 id, job, skill, loc
            FROM user_profiles
            WHERE user_id = ?
            ORDER BY created_at DESC
        """, (user_id,))
        profile_row = cursor.fetchone()

        if profile_row:
            profile_id, old_job, old_skill, old_loc = profile_row

            job = job or old_job
            skills_text = skills_text or old_skill
            ville = ville or old_loc

            cursor.execute("""
                UPDATE user_profiles
                SET job = ?, skill = ?, loc = ?
                WHERE id = ?
            """, (job, skills_text, ville, profile_id))
            message = "Profil mis à jour avec succès"
        else:
            # Aucun profil => on en crée un
            cursor.execute("""
                INSERT INTO user_profiles (user_id, job, skill, loc, blob_filename)
                VALUES (?, ?, ?, ?, ?)
            """, (user_id, job, skills_text, ville, blob_filename))
            message = "Profil créé avec succès"

        conn.commit()
        conn.close()

        return jsonify({"message": message})

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500