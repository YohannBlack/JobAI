import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

function Login() {
  const [formData, setFormData] = useState({
    prenom: '',
    nom: '',
    email: '',
  });

  const navigate = useNavigate();

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prevData) => ({
      ...prevData,
      [name]: value,
    }));
  };

  const handleLogin = (e) => {
    e.preventDefault();
    if (formData.prenom && formData.nom && formData.email) {
      localStorage.setItem('user', JSON.stringify(formData));
      navigate('/upload');
    } else {
      alert('Merci de remplir tous les champs.');
    }
  };

  return (
    <div style={styles.container}>
      <div style={styles.card}>
        <img src="/logo.png" alt="Logo JobAI" style={styles.logo} />
        <h1 style={styles.title}>Bienvenue sur JobAI</h1>
        <p style={styles.subtitle}>Connecte-toi pour continuer</p>
        <form onSubmit={handleLogin} style={styles.form}>
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
          <input
            type="email"
            name="email"
            placeholder="Email"
            value={formData.email}
            onChange={handleChange}
            style={styles.input}
          />
          <button type="submit" style={styles.button}>Se connecter</button>
        </form>
      </div>
    </div>
  );
}

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
  logo: {
    width: '140px',
    marginBottom: '20px',
    display: 'block',
    marginLeft: 'auto',
    marginRight: 'auto',
    filter: 'drop-shadow(0 0 6px rgba(0, 0, 0, 0.25))',
    backgroundColor: '#fff',
    padding: '6px',
    borderRadius: '12px',
  },
  title: {
    fontSize: '24px',
    marginBottom: '8px',
    color: '#333',
    fontWeight: '600',
  },
  subtitle: {
    fontSize: '14px',
    color: '#777',
    marginBottom: '24px',
  },
  form: {
    display: 'flex',
    flexDirection: 'column',
    gap: '14px',
  },
  input: {
    padding: '12px 14px',
    borderRadius: '8px',
    border: '1px solid #ccc',
    fontSize: '15px',
    outline: 'none',
    transition: 'border 0.3s',
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
    transition: 'background-color 0.3s',
  },
};

export default Login;
