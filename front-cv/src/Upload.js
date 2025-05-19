// src/Upload.js
import React, { useEffect, useState } from 'react';
import { getAuth, onAuthStateChanged } from 'firebase/auth';
import { getStorage, ref, uploadBytes, getDownloadURL } from 'firebase/storage';

function Upload() {
  const [user, setUser] = useState(null);
  const [file, setFile] = useState(null);
  const [url, setUrl] = useState('');
  const [cvData, setCvData] = useState(null); // ← Nouveau : pour stocker les infos extraites
  const storage = getStorage(); 
  useEffect(() => {
    const auth = getAuth();
    onAuthStateChanged(auth, (currentUser) => {
      if (currentUser) {
        setUser(currentUser);
      }
    });
  }, []);


const handleUpload = async () => {
  console.log("➡️ handleUpload déclenché !");
  if (file && user) {
    const storageRef = ref(storage, `cvs/${user.uid}_${file.name}`);
    await uploadBytes(storageRef, file);
    const downloadURL = await getDownloadURL(storageRef);
    setUrl(downloadURL);
    alert('CV téléversé avec succès !');

    // Envoi du fichier au backend Flask
    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await fetch('http://localhost:5000/extract', {
        method: 'POST',
        body: formData,
      });

      if (response.ok) {
        const data = await response.json();
        setCvData(data); // stocke les infos extraites
      } else {
        alert('Erreur lors de l\'extraction du CV');
      }
    } catch (error) {
      console.error('Erreur côté client :', error);
    }
  }
};

  return (
    <div style={styles.container}>
      <div style={styles.card}>
        <h2 style={styles.title}>Bienvenue {user?.displayName}</h2>
        <p style={styles.subtitle}>Téléverse ton CV ici (PDF uniquement)</p>

        <input
          type="file"
          accept=".pdf"
          onChange={(e) => setFile(e.target.files[0])}
          style={styles.input}
        />
        <button onClick={handleUpload} style={styles.button}>
          Uploader mon CV
        </button>

        {url && (
          <p style={styles.link}>
            ✅ Ton CV a bien été téléversé. <br />
            <a href={url} target="_blank" rel="noopener noreferrer">
              📄 Voir mon CV
            </a>
          </p>
        )}

        {cvData && (
          <div style={styles.extracted}>
            <h3>Données extraites du CV :</h3>
            <p><strong>Nom :</strong> {cvData.nom}</p>
            <p><strong>Prénom :</strong> {cvData.prenom}</p>
            <p><strong>Email :</strong> {cvData.email}</p>
            <p><strong>Téléphone :</strong> {cvData.telephone}</p>
            <p><strong>Compétences :</strong> {cvData.competences}</p>
            {/* Ajoute d'autres champs si ton backend en extrait plus */}
          </div>
        )}

        {cvData && (
          <div style={styles.cvDataBox}>
            <h3>📄 Infos extraites du CV :</h3>
            <ul>
              {Object.entries(cvData).map(([key, value]) => (
                <li key={key}><strong>{key} :</strong> {value}</li>
              ))}
            </ul>
          </div>
        )}
      </div>
    </div>
  );
}

const styles = {
  container: {
    background: 'linear-gradient(135deg, #FFDEE9, #B5FFFC)',
    height: '100vh',
    display: 'flex',
    justifyContent: 'center',
    alignItems: 'center',
    fontFamily: 'Arial, sans-serif',
  },
    extracted: {
    marginTop: '30px',
    textAlign: 'left',
    backgroundColor: '#f7f7f7',
    padding: '20px',
    borderRadius: '10px',
    color: '#333',
  },

  card: {
    backgroundColor: '#fff',
    padding: '40px',
    borderRadius: '16px',
    boxShadow: '0 12px 24px rgba(0,0,0,0.1)',
    textAlign: 'center',
    width: '500px',
  },
  title: {
    fontSize: '24px',
    marginBottom: '10px',
    color: '#333',
  },
  subtitle: {
    fontSize: '16px',
    marginBottom: '20px',
    color: '#666',
  },
  input: {
    marginBottom: '10px',
  },
  button: {
    padding: '10px 20px',
    backgroundColor: '#00C897',
    color: '#fff',
    border: 'none',
    borderRadius: '8px',
    cursor: 'pointer',
    fontSize: '16px',
  },
  link: {
    marginTop: '20px',
    color: '#0077cc',
  },
  cvDataBox: {
    marginTop: '30px',
    textAlign: 'left',
    backgroundColor: '#f0f8ff',
    padding: '20px',
    borderRadius: '10px',
  },
};

export default Upload;
