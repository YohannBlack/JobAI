import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

function Login() {
  const [isRegistering, setIsRegistering] = useState(false);
  const [formData, setFormData] = useState({
    prenom: '',
    nom: '',
    email: '',
    password: '',
    role: 'user',
  });

  const navigate = useNavigate();

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prevData) => ({
      ...prevData,
      [name]: value,
    }));
  };

const handleSubmit = (e) => {
  e.preventDefault();
  const { prenom, nom, email, password } = formData;

  if (isRegistering) {
    if (prenom && nom && email && password) {
      fetch("https://blue-grass-09f01bd03.1.azurestaticapps.ne/register", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(formData),
      })
        .then(res => res.json())
        .then(data => {
          if (data.user && data.user.id) {
            // Sauvegarder les infos utilisateur dans le localStorage
            localStorage.setItem("user_id", data.user.id);
            localStorage.setItem('user', JSON.stringify(data.user));
            alert(data.message);
            // Rediriger vers upload avec un état
            navigate('/upload', { state: { fromRegister: true } });
          } else {
            alert(data.error || "Erreur lors de l'inscription");
          }
        });
    } else {
      alert('Merci de remplir tous les champs pour créer un compte.');
      }
    } else {
      if (email && password) {
        fetch("https://blue-grass-09f01bd03.1.azurestaticapps.ne/login", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ email, password }),
        })
          .then(res => res.json())
          .then(data => {
            console.log("Réponse login :", data);
            if (data.user && data.user.id) {
              localStorage.setItem("user_id", data.user.id);
              localStorage.setItem('user', JSON.stringify(data.user));
              alert(data.message);
              navigate('/');
            } else {
              alert(data.error);
            }
          });
      } else {
        alert('Merci de remplir tous les champs pour vous connecter.');
      }
    }
  };

  return (
    <div style={styles.container}>
      <div style={styles.card}>
        <img 
          src="/logo.png" 
          alt="Logo JobAI" 
          style={styles.logo}
          onClick={() => navigate('/')}
        />
        <h1 style={styles.title}>Bienvenue sur JobAI</h1>
        <p style={styles.subtitle}>
          {isRegistering ? 'Créez votre compte' : 'Connectez-vous pour continuer'}
        </p>

        <div style={styles.toggleContainer}>
          <button
            style={{ 
              ...styles.toggleButton, 
              backgroundColor: !isRegistering ? '#e63946' : 'transparent',
              color: !isRegistering ? '#fff' : '#1f1c2c',
              border: !isRegistering ? 'none' : '2px solid #1f1c2c'
            }}
            onClick={() => setIsRegistering(false)}
          >
            Connexion
          </button>
          <button
            style={{ 
              ...styles.toggleButton, 
              backgroundColor: isRegistering ? '#e63946' : 'transparent',
              color: isRegistering ? '#fff' : '#1f1c2c',
              border: isRegistering ? 'none' : '2px solid #1f1c2c'
            }}
            onClick={() => setIsRegistering(true)}
          >
            Inscription
          </button>
        </div>

        <form onSubmit={handleSubmit} style={styles.form}>
          {isRegistering && (
            <>
              <input
                type="text"
                name="prenom"
                placeholder="Prénom"
                value={formData.prenom}
                onChange={handleChange}
                style={styles.input}
              />
              <input
                type="text"
                name="nom"
                placeholder="Nom"
                value={formData.nom}
                onChange={handleChange}
                style={styles.input}
              />
            </>
          )}
          <input
            type="email"
            name="email"
            placeholder="Email"
            value={formData.email}
            onChange={handleChange}
            style={styles.input}
          />
          <input
            type="password"
            name="password"
            placeholder="Mot de passe"
            value={formData.password}
            onChange={handleChange}
            style={styles.input}
          />
          <button 
            type="submit" 
            style={styles.button}
            onMouseOver={(e) => {
              e.currentTarget.style.transform = 'translateY(-2px)';
              e.currentTarget.style.boxShadow = '0 6px 20px rgba(230, 57, 70, 0.4)';
            }}
            onMouseOut={(e) => {
              e.currentTarget.style.transform = 'translateY(0)';
              e.currentTarget.style.boxShadow = '0 4px 15px rgba(230, 57, 70, 0.3)';
            }}
          >
            {isRegistering ? 'Créer le compte' : 'Se connecter'}
          </button>
        </form>
      </div>
    </div>
  );
}

const styles = {
  container: {
    minHeight: '100vh',
    background: 'linear-gradient(135deg, #1f1c2c 0%, #928dab 100%)',
    display: 'flex',
    justifyContent: 'center',
    alignItems: 'center',
    padding: '20px',
  },
  card: {
    backgroundColor: '#fff',
    padding: '40px',
    borderRadius: '20px',
    boxShadow: '0 10px 30px rgba(0,0,0,0.15)',
    width: '100%',
    maxWidth: '450px',
    textAlign: 'center',
    animation: 'fadeIn 0.5s ease',
  },
  logo: {
    width: '120px',
    marginBottom: '30px',
    cursor: 'pointer',
    transition: 'transform 0.3s ease',
    ':hover': {
      transform: 'scale(1.05)',
    },
  },
  title: {
    fontSize: '2rem',
    fontWeight: '700',
    marginBottom: '10px',
    color: '#1f1c2c',
    textShadow: '1px 1px 2px rgba(0,0,0,0.1)',
  },
  subtitle: {
    fontSize: '1.1rem',
    color: '#666',
    marginBottom: '30px',
    fontWeight: '500',
  },
  toggleContainer: {
    display: 'flex',
    justifyContent: 'center',
    gap: '15px',
    marginBottom: '30px',
  },
  toggleButton: {
    padding: '12px 25px',
    borderRadius: '25px',
    fontSize: '16px',
    fontWeight: '600',
    cursor: 'pointer',
    transition: 'all 0.3s ease',
    minWidth: '120px',
  },
  form: {
    display: 'flex',
    flexDirection: 'column',
    gap: '20px',
  },
  input: {
    padding: '15px 20px',
    borderRadius: '10px',
    border: '1px solid #ddd',
    fontSize: '16px',
    outline: 'none',
    transition: 'all 0.3s ease',
    ':focus': {
      borderColor: '#e63946',
      boxShadow: '0 0 0 3px rgba(230, 57, 70, 0.2)',
    },
  },
  button: {
    backgroundColor: '#e63946',
    color: '#fff',
    border: 'none',
    padding: '16px',
    borderRadius: '10px',
    fontSize: '18px',
    fontWeight: '600',
    cursor: 'pointer',
    transition: 'all 0.3s ease',
    boxShadow: '0 4px 15px rgba(230, 57, 70, 0.3)',
    marginTop: '10px',
  },
};

export default Login;