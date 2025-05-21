// src/firebase.js
import { initializeApp } from "firebase/app";
import { getAuth } from "firebase/auth";
import { getStorage } from "firebase/storage";

// Ta configuration Firebase
const firebaseConfig = {
 
};

// Initialisation de Firebase
const app = initializeApp(firebaseConfig);

// ✅ Export nommés
export const auth = getAuth(app);
export const storage = getStorage(app);
