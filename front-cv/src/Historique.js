import React, { useEffect, useState } from "react";
import Navbar from './Navbar';
import { FiExternalLink, FiHeart, FiClock } from 'react-icons/fi';

function Historique() {
  const [likedOffres, setLikedOffres] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const userId = localStorage.getItem("user_id");

  useEffect(() => {
    if (!userId) return;

    setIsLoading(true);
    fetch(`https://flask-backend-final-a2ega5c7fgcpdfah.francecentral-01.azurewebsites.net//historique_likes?user_id=${userId}`)
      .then(res => res.json())
      .then(data => {
        setLikedOffres(data);
        setIsLoading(false);
      })
      .catch(err => {
        console.error(err);
        setIsLoading(false);
      });
  }, [userId]);

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
    header: {
      display: 'flex',
      alignItems: 'center',
      marginBottom: '30px',
      color: '#fff',
    },
    title: {
      fontSize: '2rem',
      fontWeight: '700',
      marginLeft: '15px',
    },
    card: {
      backgroundColor: '#fff',
      borderRadius: '15px',
      boxShadow: '0 10px 30px rgba(0,0,0,0.15)',
      overflow: 'hidden',
    },
    emptyState: {
      padding: '40px',
      textAlign: 'center',
      color: '#666',
    },
    emptyIcon: {
      fontSize: '3rem',
      marginBottom: '20px',
      color: '#e63946',
    },
    emptyText: {
      fontSize: '1.2rem',
      marginBottom: '10px',
    },
    offerItem: {
      padding: '20px',
      borderBottom: '1px solid #f0f0f0',
      transition: 'background-color 0.3s',
      ':hover': {
        backgroundColor: '#f9f9f9',
      },
    },
    offerHeader: {
      display: 'flex',
      justifyContent: 'space-between',
      alignItems: 'center',
      marginBottom: '10px',
    },
    offerTitle: {
      fontSize: '1.3rem',
      fontWeight: '600',
      color: '#1f1c2c',
      marginBottom: '5px',
    },
    offerCompany: {
      fontSize: '1rem',
      color: '#666',
      marginBottom: '10px',
    },
    offerMeta: {
      display: 'flex',
      gap: '15px',
      marginBottom: '15px',
    },
    metaItem: {
      display: 'flex',
      alignItems: 'center',
      color: '#666',
      fontSize: '0.9rem',
    },
    metaIcon: {
      marginRight: '5px',
      color: '#e63946',
    },
    matchBadge: {
      backgroundColor: '#e63946',
      color: '#fff',
      padding: '5px 10px',
      borderRadius: '20px',
      fontSize: '0.8rem',
      fontWeight: '600',
    },
    offerLink: {
      display: 'inline-flex',
      alignItems: 'center',
      color: '#e63946',
      textDecoration: 'none',
      fontWeight: '500',
      transition: 'color 0.3s',
      ':hover': {
        color: '#c5303f',
      },
    },
    linkIcon: {
      marginLeft: '5px',
    },
    loadingContainer: {
      display: 'flex',
      justifyContent: 'center',
      alignItems: 'center',
      height: '200px',
      color: '#fff',
    },
    spinner: {
      width: '50px',
      height: '50px',
      border: '5px solid rgba(255,255,255,0.3)',
      borderRadius: '50%',
      borderTopColor: '#e63946',
      animation: 'spin 1s linear infinite',
    },
  };

  if (!userId) {
    return (
      <div style={styles.container}>
        <Navbar />
        <div style={styles.content}>
          <div style={styles.card}>
            <div style={styles.emptyState}>
              <div style={styles.emptyIcon}>🔒</div>
              <p style={styles.emptyText}>Veuillez vous connecter pour voir votre historique</p>
            </div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div style={styles.container}>
      <Navbar />
      <div style={styles.content}>
        <div style={styles.header}>
          <FiHeart size={30} />
          <h1 style={styles.title}>Votre Historique</h1>
        </div>

        <div style={styles.card}>
          {isLoading ? (
            <div style={styles.loadingContainer}>
              <div style={styles.spinner}></div>
            </div>
          ) : likedOffres.length === 0 ? (
            <div style={styles.emptyState}>
              <div style={styles.emptyIcon}>📭</div>
              <h3 style={styles.emptyText}>Aucune offre likée pour le moment</h3>
              <p>Les offres que vous likez apparaîtront ici</p>
            </div>
          ) : (
            likedOffres.map((offre) => (
              <div key={offre.offre_id} style={styles.offerItem}>
                <div style={styles.offerHeader}>
                  <span style={styles.matchBadge}>
                    {(offre.score * 100).toFixed(0)}% match
                  </span>
                </div>
                <h3 style={styles.offerTitle}>{offre.intitule}</h3>
                <p style={styles.offerCompany}>{offre.entreprise?.nom || 'Entreprise non spécifiée'}</p>
                
                <div style={styles.offerMeta}>
                  <div style={styles.metaItem}>
                    <FiClock style={styles.metaIcon} />
                    {new Date(offre.dateCreation).toLocaleDateString()}
                  </div>
                  <div style={styles.metaItem}>
                    📍 {offre.lieuTravail_libelle}
                  </div>
                </div>

                <a
                  href={offre.origineOffre_urlOrigine}
                  target="_blank"
                  rel="noreferrer"
                  style={styles.offerLink}
                >
                  Voir l'offre complète
                  <FiExternalLink style={styles.linkIcon} />
                </a>
              </div>
            ))
          )}
        </div>
      </div>

      {/* Animation CSS pour le spinner */}
      <style>{`
        @keyframes spin {
          0% { transform: rotate(0deg); }
          100% { transform: rotate(360deg); }
        }
      `}</style>
    </div>
  );
}

export default Historique;