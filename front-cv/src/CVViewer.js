import React, { useState, useEffect } from 'react';
import Navbar from './Navbar';

function CVViewer() {
  const [pdfUrl, setPdfUrl] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchCV = async () => {
      try {
        const userId = localStorage.getItem('user_id');
        if (!userId) {
          setError("Utilisateur non connecté");
          setLoading(false);
          return;
        }

        const response = await fetch(`https://flask-backend-hwagfjehhhc0hzby.francecentral-01.azurewebsites.net/cv/${userId}`);
        const data = await response.json();

        if (response.ok && data.url) {
          // Utilisation directe de l'URL du blob storage
          setPdfUrl(data.url);
        } else {
          setError(data.error || "Impossible de récupérer le CV");
        }
      } catch (err) {
        setError("Une erreur est survenue lors du chargement");
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    fetchCV();
  }, []);

  const styles = {
    container: {
      minHeight: '100vh',
      backgroundColor: '#f5f5f5',
    },
    pdfContainer: {
      height: '80vh',
      margin: '20px',
    },
    pdfViewer: {
      width: '100%',
      height: '100%',
      border: 'none',
    }
  };

  return (
    <div style={styles.container}>
      <Navbar />
      
      <div style={{ padding: '20px' }}>
        <h1>Mon CV</h1>
        
        {loading && <p>Chargement en cours...</p>}
        
        {error && (
          <div style={{ color: 'red' }}>
            {error}
            <button onClick={() => window.location.reload()}>Réessayer</button>
          </div>
        )}

        {pdfUrl && (
          <div style={styles.pdfContainer}>
            <iframe
              src={pdfUrl}
              style={styles.pdfViewer}
              title="Visualisateur de CV"
            />
          </div>
        )}
      </div>
    </div>
  );
}

export default CVViewer;