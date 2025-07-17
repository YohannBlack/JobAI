import React from 'react';
import { useNavigate } from 'react-router-dom';
import Navbar from './Navbar';

function Home() {
  const navigate = useNavigate();
  const user = JSON.parse(localStorage.getItem('user') || '{}');

  const features = [
    {
      icon: '🚀',
      title: 'Upload Intelligent',
      description: 'Notre IA analyse automatiquement votre CV et extrait les informations clés',
      action: () => navigate('/upload'),
      buttonText: 'Uploader mon CV'
    },
    {
      icon: '💼',
      title: 'Swipe & Match',
      description: 'Découvrez les offres qui correspondent à votre profil avec un système de swipe intuitif',
      action: () => navigate('/swipe'),
      buttonText: 'Voir les offres'
    },
    {
      icon: '📊',
      title: 'Suivi Personnalisé',
      description: 'Suivez vos candidatures et consultez l\'historique de vos interactions',
      action: () => navigate('/historique'),
      buttonText: 'Mon historique'
    }
  ];

  const stats = [
    { number: '10K+', label: 'Offres analysées' },
    { number: '95%', label: 'Taux de matching' },
    { number: '500+', label: 'Utilisateurs actifs' }
  ];

  const styles = {
    container: {
      minHeight: '100vh',
      background: 'linear-gradient(135deg, #1f1c2c 0%, #928dab 100%)',
    },
    heroSection: {
      padding: '60px 20px',
      textAlign: 'center',
      background: 'linear-gradient(135deg, rgba(31, 28, 44, 0.9) 0%, rgba(146, 141, 171, 0.9) 100%)',
      color: '#fff',
    },
    heroContent: {
      maxWidth: '800px',
      margin: '0 auto',
    },
    heroTitle: {
      fontSize: '3.5rem',
      fontWeight: '700',
      marginBottom: '20px',
      textShadow: '2px 2px 4px rgba(0,0,0,0.3)',
      '@media (max-width: 768px)': {
        fontSize: '2.5rem',
      },
    },
    heroSubtitle: {
      fontSize: '1.3rem',
      marginBottom: '30px',
      opacity: '0.9',
      lineHeight: '1.6',
      '@media (max-width: 768px)': {
        fontSize: '1.1rem',
      },
    },
    welcomeText: {
      fontSize: '1.5rem',
      marginBottom: '40px',
      color: '#e63946',
      fontWeight: '600',
    },
    ctaButton: {
      backgroundColor: '#e63946',
      color: '#fff',
      border: 'none',
      padding: '15px 30px',
      borderRadius: '25px',
      fontSize: '18px',
      fontWeight: '600',
      cursor: 'pointer',
      transition: 'all 0.3s ease',
      boxShadow: '0 4px 15px rgba(230, 57, 70, 0.3)',
      margin: '0 10px',
    },
    featuresSection: {
      padding: '80px 20px',
      backgroundColor: '#fff',
    },
    sectionTitle: {
      fontSize: '2.5rem',
      fontWeight: '700',
      textAlign: 'center',
      marginBottom: '50px',
      color: '#333',
    },
    featuresGrid: {
      display: 'grid',
      gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))',
      gap: '30px',
      maxWidth: '1200px',
      margin: '0 auto',
    },
    featureCard: {
      backgroundColor: '#fff',
      padding: '40px 30px',
      borderRadius: '20px',
      boxShadow: '0 10px 30px rgba(0,0,0,0.1)',
      textAlign: 'center',
      transition: 'transform 0.3s ease',
      cursor: 'pointer',
    },
    featureIcon: {
      fontSize: '3rem',
      marginBottom: '20px',
      display: 'block',
    },
    featureTitle: {
      fontSize: '1.5rem',
      fontWeight: '600',
      marginBottom: '15px',
      color: '#333',
    },
    featureDescription: {
      fontSize: '1rem',
      color: '#666',
      lineHeight: '1.6',
      marginBottom: '25px',
    },
    featureButton: {
      backgroundColor: '#1f1c2c',
      color: '#fff',
      border: 'none',
      padding: '12px 24px',
      borderRadius: '8px',
      fontSize: '14px',
      fontWeight: '500',
      cursor: 'pointer',
      transition: 'background-color 0.3s ease',
    },
    statsSection: {
      padding: '60px 20px',
      backgroundColor: '#f8f9fa',
    },
    statsGrid: {
      display: 'grid',
      gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))',
      gap: '30px',
      maxWidth: '800px',
      margin: '0 auto',
    },
    statCard: {
      textAlign: 'center',
      padding: '30px',
    },
    statNumber: {
      fontSize: '2.5rem',
      fontWeight: '700',
      color: '#e63946',
      marginBottom: '10px',
    },
    statLabel: {
      fontSize: '1.1rem',
      color: '#666',
      fontWeight: '500',
    },
    footer: {
      backgroundColor: '#1f1c2c',
      color: '#fff',
      padding: '40px 20px',
      textAlign: 'center',
    },
    footerText: {
      fontSize: '1rem',
      opacity: '0.8',
    },
  };

  return (
    <div style={styles.container}>
      <Navbar />
      
      {/* Hero Section */}
      <section style={styles.heroSection}>
        <div style={styles.heroContent}>
          <h1 style={styles.heroTitle}>
            Trouvez votre job de rêve avec l'IA
          </h1>
          <p style={styles.heroSubtitle}>
            JobAI révolutionne la recherche d'emploi en utilisant l'intelligence artificielle 
            pour matcher parfaitement votre profil avec les meilleures opportunités
          </p>
          {user.prenom && (
            <div style={styles.welcomeText}>
              Bon retour, {user.prenom} ! 👋
            </div>
          )}
          <button 
            style={styles.ctaButton}
            onClick={() => navigate('/upload')}
            onMouseOver={(e) => {
              e.currentTarget.style.transform = 'translateY(-2px)';
              e.currentTarget.style.boxShadow = '0 6px 20px rgba(230, 57, 70, 0.4)';
            }}
            onMouseOut={(e) => {
              e.currentTarget.style.transform = 'translateY(0)';
              e.currentTarget.style.boxShadow = '0 4px 15px rgba(230, 57, 70, 0.3)';
            }}
          >
            Commencer maintenant
          </button>
          <button 
            style={{...styles.ctaButton, backgroundColor: 'transparent', border: '2px solid #fff'}}
            onClick={() => navigate('/swipe')}
          >
            Voir les offres
          </button>
        </div>
      </section>

      {/* Features Section */}
      <section style={styles.featuresSection}>
        <h2 style={styles.sectionTitle}>Comment ça marche ?</h2>
        <div style={styles.featuresGrid}>
          {features.map((feature, index) => (
            <div
              key={index}
              style={styles.featureCard}
              onMouseOver={(e) => {
                e.currentTarget.style.transform = 'translateY(-5px)';
              }}
              onMouseOut={(e) => {
                e.currentTarget.style.transform = 'translateY(0)';
              }}
            >
              <span style={styles.featureIcon}>{feature.icon}</span>
              <h3 style={styles.featureTitle}>{feature.title}</h3>
              <p style={styles.featureDescription}>{feature.description}</p>
              <button
                style={styles.featureButton}
                onClick={feature.action}
                onMouseOver={(e) => e.currentTarget.style.backgroundColor = '#333'}
                onMouseOut={(e) => e.currentTarget.style.backgroundColor = '#1f1c2c'}
              >
                {feature.buttonText}
              </button>
            </div>
          ))}
        </div>
      </section>

      {/* Stats Section */}
      <section style={styles.statsSection}>
        <h2 style={styles.sectionTitle}>Nos résultats parlent d'eux-mêmes</h2>
        <div style={styles.statsGrid}>
          {stats.map((stat, index) => (
            <div key={index} style={styles.statCard}>
              <div style={styles.statNumber}>{stat.number}</div>
              <div style={styles.statLabel}>{stat.label}</div>
            </div>
          ))}
        </div>
      </section>

      {/* Footer */}
      <footer style={styles.footer}>
        <p style={styles.footerText}>
          © 2024 JobAI - Votre partenaire intelligent pour l'emploi
        </p>
      </footer>
    </div>
  );
}

export default Home;