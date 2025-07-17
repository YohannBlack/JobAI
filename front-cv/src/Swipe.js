import React, { useEffect, useState, useRef } from "react";
import { useSwipeable } from "react-swipeable";
import Navbar from './Navbar';

function Swipe() {
  const [offres, setOffres] = useState([]);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [isAnimating, setIsAnimating] = useState(false);
  const [swipeDirection, setSwipeDirection] = useState(null);
  const [isLoading, setIsLoading] = useState(true); // Nouvel état pour le chargement
  const cardRef = useRef(null);
  const userId = localStorage.getItem("user_id");

  // Chargement des offres
  useEffect(() => {
    setIsLoading(true); // Activer l'état de chargement
    fetch(`https://flask-backend-hwagfjehhhc0hzby.francecentral-01.azurewebsites.net/offres?user_id=${userId}`, {
      method: "GET",
    })
      .then((res) => res.json())
      .then((data) => {
        setOffres(data);
        setIsLoading(false); // Désactiver l'état de chargement une fois les données reçues
      })
      .catch((error) => {
        console.error("Erreur lors de la récupération des offres :", error);
        setIsLoading(false); // Désactiver l'état de chargement en cas d'erreur
      });
  }, [userId]);

  // Gestion des swipes
  const handlers = useSwipeable({
    onSwipedLeft: () => handleSwipe('left'),
    onSwipedRight: () => handleSwipe('right'),
    trackMouse: true
  });

  const handleSwipe = (direction) => {
    if (isAnimating || currentIndex >= offres.length) return;
    
    setIsAnimating(true);
    setSwipeDirection(direction);
    
    // Envoyer le feedback
    envoyerFeedback(direction === 'right' ? 1 : 0);
    
    // Passer à l'offre suivante après l'animation
    setTimeout(() => {
      setCurrentIndex(prev => prev + 1);
      setIsAnimating(false);
      setSwipeDirection(null);
    }, 300);
  };

  const envoyerFeedback = async (feedbackValue) => {
    const offre = offres[currentIndex];
    if (!offre?.id) return;

    try {
      await fetch(`https://flask-backend-hwagfjehhhc0hzby.francecentral-01.azurewebsites.net/feedback`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          offre_id: offre.id,
          user_id: Number(userId),
          feedback: feedbackValue,
        }),
      });
    } catch (error) {
      console.error("Erreur lors de l'envoi du feedback :", error);
    }
  };

  // Styles
  const styles = {
    container: {
      minHeight: '100vh',
      background: 'linear-gradient(135deg, #1f1c2c 0%, #928dab 100%)',
      paddingTop: '70px',
      paddingBottom: '40px',
    },
    content: {
      maxWidth: '500px',
      margin: '0 auto',
      padding: '20px',
      position: 'relative',
      height: 'calc(100vh - 110px)',
    },
    cardContainer: {
      position: 'relative',
      width: '100%',
      height: '70%',
      display: 'flex',
      justifyContent: 'center',
      alignItems: 'center',
    },
    card: {
      width: '100%',
      maxWidth: '400px',
      backgroundColor: '#fff',
      borderRadius: '20px',
      boxShadow: '0 10px 30px rgba(0,0,0,0.2)',
      padding: '25px',
      position: 'absolute',
      transition: 'transform 0.3s ease, opacity 0.3s ease',
      cursor: 'grab',
      userSelect: 'none',
      transform: swipeDirection ? 
        `translateX(${swipeDirection === 'right' ? '120%' : '-120%'}) rotate(${swipeDirection === 'right' ? '15deg' : '-15deg'})` : 
        'translateX(0) rotate(0)',
      opacity: swipeDirection ? '0' : '1',
    },
    cardHeader: {
      display: 'flex',
      justifyContent: 'space-between',
      alignItems: 'center',
      marginBottom: '15px',
    },
    matchScore: {
      backgroundColor: '#e63946',
      color: '#fff',
      padding: '5px 10px',
      borderRadius: '20px',
      fontSize: '14px',
      fontWeight: '600',
    },
    title: {
      fontSize: '1.8rem',
      fontWeight: '700',
      color: '#1f1c2c',
      marginBottom: '10px',
    },
    company: {
      fontSize: '1.2rem',
      color: '#666',
      marginBottom: '15px',
    },
    location: {
      display: 'flex',
      alignItems: 'center',
      color: '#777',
      marginBottom: '15px',
      fontSize: '1rem',
    },
    contract: {
      backgroundColor: '#f0f0f0',
      padding: '5px 10px',
      borderRadius: '5px',
      display: 'inline-block',
      marginBottom: '15px',
      fontSize: '0.9rem',
    },
    description: {
      color: '#444',
      lineHeight: '1.6',
      marginBottom: '20px',
      maxHeight: '150px',
      overflowY: 'auto',
    },
    buttonsContainer: {
      display: 'flex',
      justifyContent: 'center',
      gap: '20px',
      marginTop: '20px',
    },
    button: {
      width: '60px',
      height: '60px',
      borderRadius: '50%',
      border: 'none',
      cursor: 'pointer',
      display: 'flex',
      justifyContent: 'center',
      alignItems: 'center',
      boxShadow: '0 4px 10px rgba(0,0,0,0.1)',
      transition: 'transform 0.2s',
    },
    rejectButton: {
      backgroundColor: '#fff',
      color: '#e63946',
      border: '2px solid #e63946',
    },
    acceptButton: {
      backgroundColor: '#e63946',
      color: '#fff',
    },
    emptyState: {
      textAlign: 'center',
      color: '#fff',
      padding: '20px',
    },
    loadingState: {
      textAlign: 'center',
      color: '#fff',
      padding: '20px',
      display: 'flex',
      flexDirection: 'column',
      alignItems: 'center',
      justifyContent: 'center',
      height: '100%',
    },
    spinner: {
      border: '4px solid rgba(255, 255, 255, 0.3)',
      borderRadius: '50%',
      borderTop: '4px solid #e63946',
      width: '40px',
      height: '40px',
      animation: 'spin 1s linear infinite',
      marginBottom: '20px',
    },
    icon: {
      fontSize: '24px',
    },
  };

  // Ajout de l'animation du spinner
  const spinAnimation = `
    @keyframes spin {
      0% { transform: rotate(0deg); }
      100% { transform: rotate(360deg); }
    }
  `;

  if (currentIndex >= offres.length && !isLoading) {
    return (
      <div style={styles.container}>
        <Navbar />
        <div style={styles.emptyState}>
          <h2>Vous avez vu toutes les offres ! </h2>
          <p>Revenez plus tard pour de nouvelles opportunités</p>
        </div>
      </div>
    );
  }

  // Afficher l'état de chargement
  if (isLoading) {
    return (
      <div style={styles.container}>
        <style>{spinAnimation}</style>
        <Navbar />
        <div style={styles.loadingState}>
          <div style={styles.spinner}></div>
          <h2>Chargement des offres...</h2>
          <p>Veuillez patienter pendant que nous trouvons les meilleures offres pour vous</p>
        </div>
      </div>
    );
  }

  const currentOffer = offres[currentIndex];

  return (
    <div style={styles.container}>
      <Navbar />
      <div style={styles.content}>
        <div style={styles.cardContainer} {...handlers}>
          {currentOffer && (
            <div 
              ref={cardRef} 
              style={styles.card}
              onClick={() => window.open(currentOffer.origineOffre_urlOrigine, '_blank')}
            >
              <div style={styles.cardHeader}>
                <div style={styles.matchScore}>
                  {(currentOffer.score * 100).toFixed(0)}% match
                </div>
                <div style={styles.contract}>
                  {currentOffer.typeContrat}
                </div>
              </div>
              <h2 style={styles.title}>{currentOffer.intitule}</h2>
              <p style={styles.company}>{currentOffer.entreprise?.nom || 'Entreprise non spécifiée'}</p>
              <div style={styles.location}>
                📍 {currentOffer.lieuTravail_libelle}
              </div>
              <div style={styles.description}>
                {currentOffer.description || 'Aucune description disponible'}
              </div>
            </div>
          )}
        </div>

        <div style={styles.buttonsContainer}>
          <button
            style={{ ...styles.button, ...styles.rejectButton }}
            onClick={() => handleSwipe('left')}
            disabled={isAnimating}
          >
            <span style={styles.icon}>✖</span>
          </button>
          <button
            style={{ ...styles.button, ...styles.acceptButton }}
            onClick={() => handleSwipe('right')}
            disabled={isAnimating}
          >
            <span style={styles.icon}>✓</span>
          </button>
        </div>
      </div>
    </div>
  );
}

export default Swipe;