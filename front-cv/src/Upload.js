import React, { useState, useEffect } from "react";
import { useNavigate, useLocation } from "react-router-dom";
import Navbar from './Navbar';

function Upload() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [cvData, setCvData] = useState(null);
  const [user, setUser] = useState({ prenom: '', nom: '', email: '' });
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false); // Nouvel état pour le chargement
  const userId = localStorage.getItem("user_id");
  const navigate = useNavigate();
  const location = useLocation();

  useEffect(() => {
    const savedUser = localStorage.getItem('user');
    if (savedUser) {
      const userData = JSON.parse(savedUser);
      setUser(userData);
      
      if (location.state?.fromRegister) {
        setError('Veuillez uploader votre CV pour compléter votre profil');
      }
    } else {
      navigate('/login');
    }
  }, [location.state, navigate]);

  const handleFileChange = (event) => {
    setSelectedFile(event.target.files[0]);
    setError('');
  };

  const handleUpload = async (e) => {
    e.preventDefault();

    if (!selectedFile) {
      setError("Veuillez sélectionner un fichier PDF");
      return;
    }

    setIsLoading(true); // Activer l'état de chargement
    setError('');

    const formData = new FormData();
    formData.append("file", selectedFile);
    formData.append("userId", userId);

    try {
      const response = await fetch("https://flask-backend-final-a2ega5c7fgcpdfah.francecentral-01.azurewebsites.net//extract", {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        throw new Error("Erreur lors de l'extraction");
      }

      const data = await response.json();
      
      if (data.entities) {
        const emailEntity = data.entities.find(e => e.label.toLowerCase() === 'email');
        if (emailEntity && emailEntity.text !== user.email) {
          setError("L'email du CV ne correspond pas à votre email de connexion");
          setIsLoading(false);
          return;
        }
      }

      console.log("Réponse du backend :", data);
      navigate("/review", { state: { cvData: data } });
    } catch (error) {
      console.error("Erreur :", error);
      setError("Une erreur est survenue lors de l'upload");
    } finally {
      setIsLoading(false); // Désactiver l'état de chargement dans tous les cas
    }
  };

  const styles = {
    container: {
      minHeight: '100vh',
      background: 'linear-gradient(135deg, #1f1c2c 0%, #928dab 100%)',
      paddingTop: '70px',
    },
    content: {
      maxWidth: '800px',
      margin: '0 auto',
      padding: '40px 20px',
    },
    card: {
      backgroundColor: '#fff',
      padding: '40px',
      borderRadius: '20px',
      boxShadow: '0 10px 30px rgba(0,0,0,0.15)',
      textAlign: 'center',
    },
    title: {
      fontSize: '2rem',
      fontWeight: '700',
      marginBottom: '10px',
      color: '#1f1c2c',
    },
    subtitle: {
      fontSize: '1.1rem',
      color: '#666',
      marginBottom: '30px',
    },
    fileInputContainer: {
      margin: '30px 0',
    },
    fileInput: {
      width: '0.1px',
      height: '0.1px',
      opacity: '0',
      overflow: 'hidden',
      position: 'absolute',
      zIndex: '-1',
    },
    fileInputLabel: {
      backgroundColor: '#e63946',
      color: '#fff',
      padding: '15px 30px',
      borderRadius: '25px',
      fontSize: '18px',
      fontWeight: '600',
      cursor: 'pointer',
      transition: 'all 0.3s ease',
      boxShadow: '0 4px 15px rgba(230, 57, 70, 0.3)',
      display: 'inline-block',
      ':hover': {
        transform: 'translateY(-2px)',
        boxShadow: '0 6px 20px rgba(230, 57, 70, 0.4)',
      },
    },
    fileName: {
      marginTop: '15px',
      fontSize: '14px',
      color: '#666',
    },
    button: {
      backgroundColor: '#1f1c2c',
      color: '#fff',
      border: 'none',
      padding: '15px 30px',
      borderRadius: '25px',
      fontSize: '18px',
      fontWeight: '600',
      cursor: 'pointer',
      transition: 'all 0.3s ease',
      boxShadow: '0 4px 15px rgba(0,0,0,0.1)',
      marginTop: '20px',
      ':hover': {
        backgroundColor: '#333',
        transform: 'translateY(-2px)',
      },
      ':disabled': {
        backgroundColor: '#ccc',
        cursor: 'not-allowed',
        transform: 'none',
      },
    },
    error: {
      color: '#e63946',
      margin: '20px 0',
      fontWeight: '500',
    },
    userInfo: {
      backgroundColor: '#f8f9fa',
      padding: '20px',
      borderRadius: '10px',
      marginBottom: '30px',
      textAlign: 'left',
    },
    infoText: {
      margin: '5px 0',
      color: '#333',
    },
    loadingContainer: {
      margin: '30px 0',
      textAlign: 'center',
    },
    spinner: {
      border: '4px solid rgba(31, 28, 44, 0.1)',
      borderTop: '4px solid #1f1c2c',
      borderRadius: '50%',
      width: '40px',
      height: '40px',
      animation: 'spin 1s linear infinite',
      margin: '0 auto',
    },
    loadingText: {
      marginTop: '15px',
      color: '#1f1c2c',
      fontWeight: '500',
    },
  };

  // Animation CSS pour le spinner
  const spinAnimation = `
    @keyframes spin {
      0% { transform: rotate(0deg); }
      100% { transform: rotate(360deg); }
    }
  `;

  return (
    <div style={styles.container}>
      <style>{spinAnimation}</style>
      <Navbar />
      
      <div style={styles.content}>
        <div style={styles.card}>
          <h1 style={styles.title}>Uploader votre CV</h1>
          <p style={styles.subtitle}>
            {user.prenom ? `Bienvenue ${user.prenom} ${user.nom}` : 'Complétez votre profil'}
          </p>

          <div style={styles.userInfo}>
            <p style={styles.infoText}><strong>Email enregistré :</strong> {user.email}</p>
            <p style={styles.infoText}>Votre CV doit contenir cet email pour vérification</p>
          </div>

          {error && <div style={styles.error}>{error}</div>}

          {isLoading ? (
            <div style={styles.loadingContainer}>
              <div style={styles.spinner}></div>
              <p style={styles.loadingText}>Analyse de votre CV en cours...</p>
            </div>
          ) : (
            <>
              <div style={styles.fileInputContainer}>
                <input
                  type="file"
                  id="fileInput"
                  accept=".pdf"
                  onChange={handleFileChange}
                  style={styles.fileInput}
                />
                <label htmlFor="fileInput" style={styles.fileInputLabel}>
                  Sélectionner un fichier PDF
                </label>
                {selectedFile && (
                  <div style={styles.fileName}>
                    Fichier sélectionné : {selectedFile.name}
                  </div>
                )}
              </div>

              <button 
                onClick={handleUpload} 
                style={styles.button}
                disabled={!selectedFile || isLoading}
              >
                Analyser mon CV
              </button>
            </>
          )}
        </div>
      </div>
    </div>
  );
}

export default Upload;