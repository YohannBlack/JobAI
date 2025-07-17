import React, { useState } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';

function Navbar() {
  const navigate = useNavigate();
  const location = useLocation();
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  
  const user = JSON.parse(localStorage.getItem('user') || '{}');

  const handleLogout = () => {
    localStorage.removeItem('user_id');
    localStorage.removeItem('user');
    navigate('/');
  };

  const menuItems = [
    { path: '/upload', label: 'Upload CV', icon: '📄' },
    { path: '/swipe', label: 'Swiper', icon: '💼' },
    { path: '/historique', label: 'Historique', icon: '📋' },
     { path: '/cv', label: 'Mon CV', icon: '👁️' },
  ];

  const styles = {
    navbar: {
      backgroundColor: '#1f1c2c',
      padding: '0 20px',
      position: 'fixed',
      top: 0,
      left: 0,
      right: 0,
      zIndex: 1000,
      boxShadow: '0 2px 10px rgba(0,0,0,0.1)',
    },
    navContent: {
      display: 'flex',
      justifyContent: 'space-between',
      alignItems: 'center',
      maxWidth: '1200px',
      margin: '0 auto',
      height: '70px',
    },
    logo: {
      height: '40px',
      cursor: 'pointer',
    },
    desktopMenu: {
      display: 'flex',
      gap: '30px',
      alignItems: 'center',
      '@media (max-width: 768px)': {
        display: 'none',
      },
    },
    menuItem: {
      color: '#fff',
      textDecoration: 'none',
      padding: '10px 15px',
      borderRadius: '8px',
      transition: 'all 0.3s ease',
      display: 'flex',
      alignItems: 'center',
      gap: '8px',
      fontSize: '14px',
      fontWeight: '500',
    },
    activeItem: {
      backgroundColor: '#e63946',
      color: '#fff',
    },
    userInfo: {
      display: 'flex',
      alignItems: 'center',
      gap: '15px',
      color: '#fff',
    },
    userAvatar: {
      width: '35px',
      height: '35px',
      borderRadius: '50%',
      backgroundColor: '#e63946',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      fontWeight: 'bold',
      fontSize: '14px',
    },
    logoutBtn: {
      backgroundColor: '#e63946',
      color: '#fff',
      border: 'none',
      padding: '8px 16px',
      borderRadius: '6px',
      cursor: 'pointer',
      fontSize: '14px',
      fontWeight: '500',
      transition: 'background-color 0.3s ease',
    },
    mobileMenuBtn: {
      display: 'none',
      backgroundColor: 'transparent',
      border: 'none',
      color: '#fff',
      fontSize: '24px',
      cursor: 'pointer',
      '@media (max-width: 768px)': {
        display: 'block',
      },
    },
    mobileMenu: {
      position: 'fixed',
      top: '70px',
      left: 0,
      right: 0,
      backgroundColor: '#1f1c2c',
      padding: '20px',
      transform: isMenuOpen ? 'translateY(0)' : 'translateY(-100%)',
      transition: 'transform 0.3s ease',
      boxShadow: '0 2px 10px rgba(0,0,0,0.1)',
    },
    mobileMenuItem: {
      display: 'block',
      color: '#fff',
      textDecoration: 'none',
      padding: '15px 0',
      borderBottom: '1px solid #333',
      fontSize: '16px',
      fontWeight: '500',
    },
    mobileUserSection: {
      borderTop: '1px solid #333',
      paddingTop: '20px',
      marginTop: '20px',
      display: 'flex',
      justifyContent: 'space-between',
      alignItems: 'center',
    },
  };

  return (
    <>
      <nav style={styles.navbar}>
        <div style={styles.navContent}>
          <img 
            src="/logo.png" 
            alt="JobAI" 
            style={styles.logo}
            onClick={() => navigate('/')}
          />
          
          {/* Desktop Menu */}
          <div style={styles.desktopMenu}>
            {menuItems.map((item) => (
              <a
                key={item.path}
                href="#"
                onClick={(e) => {
                  e.preventDefault();
                  navigate(item.path);
                }}
                style={{
                  ...styles.menuItem,
                  ...(location.pathname === item.path ? styles.activeItem : {}),
                }}
              >
                <span>{item.icon}</span>
                {item.label}
              </a>
            ))}
          </div>

          {/* Desktop User Info */}
          <div style={styles.userInfo}>
            <div style={styles.userAvatar}>
              {user.prenom ? user.prenom[0].toUpperCase() : 'U'}
            </div>
            <span style={{ fontSize: '14px', display: window.innerWidth > 768 ? 'block' : 'none' }}>
              {user.prenom} {user.nom}
            </span>
            <button 
              onClick={handleLogout}
              style={styles.logoutBtn}
              onMouseOver={(e) => e.currentTarget.style.backgroundColor = '#c5303f'}
              onMouseOut={(e) => e.currentTarget.style.backgroundColor = '#e63946'}
            >
              Déconnexion
            </button>
          </div>

          {/* Mobile Menu Button */}
          <button 
            style={styles.mobileMenuBtn}
            onClick={() => setIsMenuOpen(!isMenuOpen)}
          >
            ☰
          </button>
        </div>
      </nav>

      {/* Mobile Menu */}
      <div style={styles.mobileMenu}>
        {menuItems.map((item) => (
          <a
            key={item.path}
            href="#"
            onClick={(e) => {
              e.preventDefault();
              navigate(item.path);
              setIsMenuOpen(false);
            }}
            style={{
              ...styles.mobileMenuItem,
              ...(location.pathname === item.path ? { color: '#e63946' } : {}),
            }}
          >
            {item.icon} {item.label}
          </a>
        ))}
        
        <div style={styles.mobileUserSection}>
          <span style={{ color: '#fff' }}>
            {user.prenom} {user.nom}
          </span>
          <button 
            onClick={handleLogout}
            style={styles.logoutBtn}
          >
            Déconnexion
          </button>
        </div>
      </div>

      {/* Spacer for fixed navbar */}
      <div style={{ height: '70px' }} />
    </>
  );
}

export default Navbar;