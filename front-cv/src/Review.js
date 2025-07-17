import React, { useEffect, useState } from "react";
import { useNavigate, useLocation } from "react-router-dom";
import Navbar from './Navbar';
import { FiCheck, FiEdit2, FiArrowRight } from 'react-icons/fi';

function Review() {
  const navigate = useNavigate();
  const location = useLocation();
  const [cvData, setCvData] = useState(location.state?.cvData || null);
  const [isSubmitting, setIsSubmitting] = useState(false);

  useEffect(() => {
    if (!cvData) {
      navigate("/upload");
    }
  }, [cvData, navigate]);

  const handleEntityChange = (label, value) => {
    const updatedEntities = [...cvData.entities];
    const index = updatedEntities.findIndex(e => e.label === label);

    if (index !== -1) {
      updatedEntities[index].text = value;
    } else {
      updatedEntities.push({ label, text: value });
    }

    setCvData({ ...cvData, entities: updatedEntities });
  };
  const handleGoSwipe = async () => {
    setIsSubmitting(true);
    try {
      const response = await fetch("https://blue-grass-09f01bd03.1.azurestaticapps.ne/update-profile", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          entities: cvData.entities,
          blob_filename: cvData.blob_filename,
        }),
      });

      if (!response.ok) {
        throw new Error("Erreur lors de la mise à jour du profil");
      }

      navigate("/swipe");
    } catch (error) {
      console.error("Erreur :", error);
      setIsSubmitting(false);
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
      borderRadius: '15px',
      boxShadow: '0 10px 30px rgba(0,0,0,0.15)',
      padding: '30px',
    },
    header: {
      display: 'flex',
      alignItems: 'center',
      marginBottom: '30px',
    },
    title: {
      fontSize: '2rem',
      fontWeight: '700',
      color: '#1f1c2c',
      marginLeft: '15px',
    },
    section: {
      marginBottom: '30px',
    },
    sectionTitle: {
      fontSize: '1.2rem',
      fontWeight: '600',
      color: '#1f1c2c',
      marginBottom: '15px',
      display: 'flex',
      alignItems: 'center',
    },
    sectionIcon: {
      marginRight: '10px',
      color: '#e63946',
    },
    formGroup: {
      marginBottom: '20px',
    },
    label: {
      display: 'block',
      fontWeight: '500',
      marginBottom: '8px',
      color: '#555',
    },
    input: {
      width: '100%',
      padding: '12px 15px',
      borderRadius: '8px',
      border: '1px solid #ddd',
      fontSize: '16px',
      transition: 'all 0.3s',
      ':focus': {
        borderColor: '#e63946',
        boxShadow: '0 0 0 3px rgba(230, 57, 70, 0.2)',
        outline: 'none',
      },
    },
    skillsList: {
      display: 'flex',
      flexWrap: 'wrap',
      gap: '10px',
      marginTop: '10px',
    },
    skillItem: {
      backgroundColor: '#f0f0f0',
      padding: '8px 15px',
      borderRadius: '20px',
      fontSize: '14px',
      display: 'flex',
      alignItems: 'center',
    },
    skillIcon: {
      marginRight: '5px',
      color: '#e63946',
    },
    button: {
      backgroundColor: '#e63946',
      color: '#fff',
      border: 'none',
      padding: '15px 30px',
      borderRadius: '8px',
      fontSize: '16px',
      fontWeight: '600',
      cursor: 'pointer',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      marginTop: '30px',
      width: '100%',
      transition: 'all 0.3s',
      ':hover': {
        backgroundColor: '#c5303f',
        transform: 'translateY(-2px)',
      },
      ':disabled': {
        backgroundColor: '#ccc',
        cursor: 'not-allowed',
        transform: 'none',
      },
    },
    buttonIcon: {
      marginLeft: '10px',
    },
    summaryCard: {
      backgroundColor: '#f8f9fa',
      padding: '20px',
      borderRadius: '10px',
      marginTop: '30px',
    },
    summaryText: {
      lineHeight: '1.6',
      color: '#444',
    },
  };

  if (!cvData) {
    return (
      <div style={styles.container}>
        <Navbar />
        <div style={styles.content}>
          <div style={styles.card}>
            <p>Chargement en cours...</p>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div style={styles.container}>
      <Navbar />
      <div style={styles.content}>
        <div style={styles.card}>
          <div style={styles.header}>
            <FiEdit2 size={30} color="#e63946" />
            <h1 style={styles.title}>Vérifiez vos informations</h1>
          </div>

          <div style={styles.section}>
            <h2 style={styles.sectionTitle}>
              <FiCheck style={styles.sectionIcon} />
              Informations personnelles
            </h2>

            <div style={styles.formGroup}>
              <label style={styles.label}>Nom complet</label>
              <input
                type="text"
                value={cvData.entities.find(e => e.label === "PER")?.text || ""}
                onChange={(e) => handleEntityChange("PER", e.target.value)}
                style={styles.input}
              />
            </div>

            <div style={styles.formGroup}>
              <label style={styles.label}>Email</label>
              <input
                type="email"
                value={cvData.entities.find(e => e.label === "EMAIL")?.text || ""}
                onChange={(e) => handleEntityChange("EMAIL", e.target.value)}
                style={styles.input}
              />
            </div>

            <div style={styles.formGroup}>
              <label style={styles.label}>Téléphone</label>
              <input
                type="tel"
                value={cvData.entities.find(e => e.label === "PHONE")?.text || ""}
                onChange={(e) => handleEntityChange("PHONE", e.target.value)}
                style={styles.input}
              />
            </div>

            <div style={styles.formGroup}>
              <label style={styles.label}>Localisation</label>
              <input
                type="text"
                value={cvData.entities.find(e => e.label === "LOC")?.text || ""}
                onChange={(e) => handleEntityChange("LOC", e.target.value)}
                style={styles.input}
              />
            </div>
          </div>

          <div style={styles.section}>
            <h2 style={styles.sectionTitle}>
              <FiCheck style={styles.sectionIcon} />
              Compétences principales
            </h2>
            <div style={styles.skillsList}>
              {cvData.entities
                .filter(e => e.label === "MISC")
                .map((skill, index) => (
                  <div key={index} style={styles.skillItem}>
                    <FiCheck style={styles.skillIcon} size={14} />
                    {skill.text}
                  </div>
                ))}
            </div>
          </div>

          {cvData?.summary && (
            <div style={styles.summaryCard}>
              <h2 style={styles.sectionTitle}>
                <FiCheck style={styles.sectionIcon} />
                Résumé de votre profil
              </h2>
              <p style={styles.summaryText}>{cvData.summary}</p>
            </div>
          )}

          <button 
            onClick={handleGoSwipe} 
            style={styles.button}
            disabled={isSubmitting}
          >
            {isSubmitting ? 'Enregistrement...' : 'Continuer vers les offres'}
            <FiArrowRight style={styles.buttonIcon} />
          </button>
        </div>
      </div>
    </div>
  );
}

export default Review;