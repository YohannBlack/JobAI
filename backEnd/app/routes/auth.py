import hashlib

import pyodbc
from flask import Blueprint, jsonify, request

from app.utils.db import get_connection

auth_bp = Blueprint("auth", __name__)  # Un seul blueprint pour tout ce module


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

@auth_bp.route("/test", methods=["GET"])
def test():
    return jsonify({"message": "OK"}), 200

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.json
    prenom = data.get('prenom')
    nom = data.get('nom')
    email = data.get('email')
    password = hash_password(data.get('password'))

    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (prenom, nom, email, password) VALUES (?, ?, ?, ?)",
                       (prenom, nom, email, password))
        conn.commit()
        return jsonify({"message": "Compte créé avec succès"}), 201
    except pyodbc.IntegrityError:
        return jsonify({"error": "Email déjà utilisé"}), 400
    except Exception as e:
        return jsonify({"error": f"Erreur base de données : {str(e)}"}), 500
    finally:
        if conn:
            conn.close()



@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = hash_password(data.get('password'))

    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, prenom, nom FROM users WHERE email = ? AND password = ?", (email, password))
        user = cursor.fetchone()
    except Exception as e:
        return jsonify({"error": f"Erreur base de données : {str(e)}"}), 500

    if user:
        return jsonify({
            "message": "Connexion réussie",
            "user": {
                "id": user[0],
                "prenom": user[1],
                "nom": user[2],
                "email": email
            }
        })
    else:
        return jsonify({"error": "Email ou mot de passe invalide"}), 401
        return jsonify({"error": "Email ou mot de passe invalide"}), 401
