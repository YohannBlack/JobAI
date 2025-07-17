import React from 'react';
import { useNavigate } from 'react-router-dom';

export default function Dashboard() {
  const navigate = useNavigate();

  const handleGoSwipe = () => navigate('/swipe');
  const handleGoUpload = () => navigate('/upload');
  const handleGoHistorique = () => navigate('/historique');

  const handleSeeCV = async () => {
    try {
      const userId = localStorage.getItem('user_id');
      if (!userId) {
        alert("Utilisateur non connecté.");
        return;
      }

      const response = await fetch(`${process.env.REACT_APP_BACK_URL}/cv/${userId}`, {
        method: "GET",
      });
      const data = await response.json();

      if (response.ok && data.url) {
        window.open(data.url, '_blank');
      } else {
        alert(data.error || "Impossible de récupérer le CV.");
      }
    } catch (error) {
      console.error("Erreur lors de la récupération du CV :", error);
      alert("Une erreur est survenue.");
    }
  };

  const styles = {
    container: {
      background: 'linear-gradient(135deg, #1f1c2c, #928dab)',
      minHeight: '100vh',
      display: 'flex',
      justifyContent: 'center',
      alignItems: 'center',
      padding: '20px',
    },
    card: {
      backgroundColor: '#ffffff',
      padding: '40px 30px',
      borderRadius: '16px',
      boxShadow: '0 10px 30px rgba(0, 0, 0, 0.1)',
      width: '100%',
      maxWidth: '400px',
      textAlign: 'center',
    },
    subtitle: {
      fontSize: '18px',
      color: '#333',
      marginBottom: '30px',
      fontWeight: '600',
    },
    button: {
      backgroundColor: '#e63946',
      color: '#fff',
      border: 'none',
      padding: '12px',
      borderRadius: '8px',
      fontSize: '16px',
      cursor: 'pointer',
      fontWeight: 'bold',
      width: '100%',
      marginBottom: '15px',
      transition: 'background-color 0.3s ease',
    }
  };

  return (
    <div style={styles.container}>
      <div style={styles.card}>
        <p style={styles.subtitle}>Vous avez déjà un CV enregistré.</p>

        <button
          style={styles.button}
          onClick={handleSeeCV}
          onMouseOver={e => e.currentTarget.style.backgroundColor = '#c5303f'}
          onMouseOut={e => e.currentTarget.style.backgroundColor = '#e63946'}
        >
          Voir mon CV
        </button>

        <button
          style={styles.button}
          onClick={handleGoSwipe}
          onMouseOver={e => e.currentTarget.style.backgroundColor = '#c5303f'}
          onMouseOut={e => e.currentTarget.style.backgroundColor = '#e63946'}
        >
          Voir les offres (Swipe)
        </button>

        <button
          style={styles.button}
          onClick={handleGoUpload}
          onMouseOver={e => e.currentTarget.style.backgroundColor = '#c5303f'}
          onMouseOut={e => e.currentTarget.style.backgroundColor = '#e63946'}
        >
          Uploader un nouveau CV
        </button>

        <button
          style={styles.button}
          onClick={handleGoHistorique}
          onMouseOver={e => e.currentTarget.style.backgroundColor = '#c5303f'}
          onMouseOut={e => e.currentTarget.style.backgroundColor = '#e63946'}
        >
          Voir mon historique
        </button>
      </div>
    </div>
  );
}
