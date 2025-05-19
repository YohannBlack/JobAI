// src/firebase.js
import { initializeApp } from "firebase/app";
import { getAuth } from "firebase/auth";
import { getStorage } from "firebase/storage";

// Ta configuration Firebase
const firebaseConfig = {
  apiKey: "AIzaSyBjfc2-f3K0WRFbIIb94j_fC4bSPPQZfe0",
  authDomain: "cv-parser-de1d2.firebaseapp.com",
  projectId: "cv-parser-de1d2",
  storageBucket: "cv-parser-de1d2.appspot.com",
  messagingSenderId: "1000134545680",
  appId: "1:1000134545680:web:5e02e42d5e55b8e5f49595"
};

// Initialisation de Firebase
const app = initializeApp(firebaseConfig);

// ✅ Export nommés
export const auth = getAuth(app);
export const storage = getStorage(app);
