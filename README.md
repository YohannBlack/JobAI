# ENDGAME
PA 2024/2025 ESGI

# 📄 CV Extractor App

Application web permettant aux utilisateurs authentifiés de téléverser leur CV (PDF), de le stocker sur Firebase Storage, et d’extraire automatiquement les informations clés grâce à un backend Flask.

---

## 🔐 Authentification avec Firebase

Ce projet utilise Firebase Authentication (via Google Login) pour identifier les utilisateurs.

### 🎯 Étapes de configuration :

1. **Créer un projet Firebase**  
   👉 [https://console.firebase.google.com](https://console.firebase.google.com)

2. **Activer l’authentification Google**  
   - Menu Firebase Console → **Authentication**
   - Onglet **"Méthode de connexion"**
   - Cliquer sur **Google** → **Activer**
   - Ajouter `http://localhost:3000` dans les **domaines autorisés**

3. **Récupérer la configuration de l’app Web Firebase**
   - Dans **Paramètres du projet** → onglet **"Général"**
   - Section **"Vos applications"** → Créer une app Web si ce n’est pas déjà fait
   - Copier ce type de configuration :

```js
const firebaseConfig = {
  apiKey: "AIza...xyz",
  authDomain: "votre-projet.firebaseapp.com",
  projectId: "votre-projet",
  storageBucket: "votre-projet.appspot.com",
  messagingSenderId: "123456789",
  appId: "1:123456789:web:abcxyz"
};

Lancer Flask (backend)	python app.py
Lancement de l'application React npm start
