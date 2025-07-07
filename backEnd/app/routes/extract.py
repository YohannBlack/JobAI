from flask import Blueprint, request, jsonify
from app.utils.db import get_connection
from app.utils.text_processing import preprocess_text, clean_entities, extract_emails, extract_phones
from app.utils.ner import ner_pipeline
from app.utils.summarizer import generate_profile_summary
from app.services.extract_text import extract_text_from_pdf
from app.services.ner_processing import extract_entities
from app.services.profil_builder import profil_to_text, construire_profil
import tempfile, uuid, os
from datetime import datetime
from app.config import container_client

extract_bp = Blueprint("extract", __name__)

@extract_bp.route('/extract', methods=['POST'])
def extract():
    if 'file' not in request.files:
        return jsonify({'error': 'Aucun fichier envoyé'}), 400
    file = request.files['file']
    if not file or file.filename == '':
        return jsonify({'error': 'Aucun fichier sélectionné'}), 400

    try:
        # Enregistrement du fichier
        timestamp = datetime.utcnow().strftime('%Y%m%d%H%M%S')
        unique_id = uuid.uuid4().hex
        extension = os.path.splitext(file.filename)[1]
        blob_filename = f"{timestamp}_{unique_id}{extension}"

        file.seek(0)
        container_client.upload_blob(name=blob_filename, data=file, overwrite=True)

        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            file.seek(0)
            tmp.write(file.read())
            tmp_path = tmp.name

        # Extraction et NER
        result = extract_text_from_pdf(tmp_path)
        result_preprocess = preprocess_text(result)
        ner_results = ner_pipeline(result_preprocess)

        def remap_entity(e):
            word = e['word'].lower()
            if "chargé" in word or "assistant" in word or "chef" in word:
                return "JOB"
            elif "communication" in word or "gestion" in word or "digital" in word:
                return "SKILL"
            else:
                return e['entity_group']

        df_entities = [(remap_entity(ent), ent['word']) for ent in ner_results]
        emails = extract_emails(result_preprocess)
        phones = extract_phones(result_preprocess)

        df_entities += [('EMAIL', email) for email in emails]
        df_entities += [('PHONE', phone) for phone in phones]

        profil = construire_profil(df_entities)
        global profil_text
        profil_text = profil_to_text(profil)

        profil_summary = generate_profile_summary(profil_text)

        entities_list = [{"label": label, "text": text} for (label, text) in df_entities]

        # Récupération des infos utiles
        email = next((text for label, text in df_entities if label == "EMAIL"), None)
        ville = next((text for label, text in df_entities if label == "CITY"), None)
        job = next((text for label, text in df_entities if label == "JOB"), None)
        skills = [text for label, text in df_entities if label == "SKILL"]
        skills_text = ", ".join(set(skills)) if skills else None
        print(entities_list)

        # Enregistrement dans la base
        if email:
            conn = get_connection()
            cursor = conn.cursor()

            # Récupérer l'id de l'utilisateur via l'email
            cursor.execute("SELECT id FROM users WHERE email = ?", (email,))
            user_row = cursor.fetchone()

            if user_row:
                user_id = user_row[0]

                # Insertion dans la table user_profiles
                cursor.execute("""
                    INSERT INTO user_profiles (user_id, job, skill, loc, blob_filename)
                    VALUES (?, ?, ?, ?, ?)
                """, (user_id, job, skills_text, ville, blob_filename))

                conn.commit()
            else:
                print(f"Aucun utilisateur trouvé avec l’email {email}")
                # Optionnel : tu peux créer automatiquement un utilisateur ici si besoin

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
