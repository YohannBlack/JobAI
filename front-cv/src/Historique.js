import React, { useEffect, useState } from "react";

function Historique() {
  const [likedOffres, setLikedOffres] = useState([]);
  const userId = localStorage.getItem("user_id");

  useEffect(() => {
    if (!userId) return;

    fetch(`https://172.189.14.214/historique_likes?user_id=${userId}`, {
      method: "GET",
      mode: "cors",
    })
      .then((res) => res.json())
      .then((data) => {
        setLikedOffres(data);
      })
      .catch((err) => console.error(err));
  }, [userId]);

  if (!userId) {
    return (
      <div style={styles.container}>
        <div style={styles.card}>
          <p>Veuillez vous connecter</p>
        </div>
      </div>
    );
  }

  return (
    <div style={styles.container}>
      <div style={styles.card}>
        <h2 style={styles.title}>Offres que vous avez likées</h2>
        {likedOffres.length === 0 ? (
          <p style={styles.subtitle}>Aucune offre likée pour le moment.</p>
        ) : (
          <ul style={styles.list}>
            {likedOffres.map((offre) => (
              <li key={offre.offre_id} style={styles.listItem}>
                <strong style={styles.offreTitle}>{offre.intitule}</strong> - <span style={styles.offreLieu}>{offre.lieuTravail_libelle}</span>
                <br />
                <a
                  href={offre.origineOffre_urlOrigine}
                  target="_blank"
                  rel="noreferrer"
                  style={styles.link}
                >
                  Voir l'offre
                </a>
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  );
}

const styles = {
  container: {
    background: 'linear-gradient(135deg, #1f1c2c, #928dab)',
    minHeight: '100vh',
    padding: '20px',
    display: 'flex',
    justifyContent: 'center',
    alignItems: 'flex-start',
  },
  card: {
    backgroundColor: '#fff',
    padding: '40px 30px',
    borderRadius: '16px',
    boxShadow: '0 10px 30px rgba(0, 0, 0, 0.1)',
    width: '100%',
    maxWidth: '600px',
    color: '#333',
  },
  title: {
    fontSize: '24px',
    marginBottom: '20px',
    fontWeight: '700',
    textAlign: 'center',
  },
  subtitle: {
    fontSize: '16px',
    color: '#666',
    textAlign: 'center',
  },
  list: {
    listStyle: 'none',
    padding: 0,
  },
  listItem: {
    marginBottom: '20px',
    paddingBottom: '10px',
    borderBottom: '1px solid #ddd',
    fontSize: '16px',
  },
  offreTitle: {
    color: '#e63946',
  },
  offreLieu: {
    color: '#555',
    fontStyle: 'italic',
  },
  link: {
    color: '#2196F3',
    textDecoration: 'none',
    fontWeight: '600',
    marginTop: '4px',
    display: 'inline-block',
  },
};

export default Historique;
