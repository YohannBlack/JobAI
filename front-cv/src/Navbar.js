import React, { useState } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';

function Navbar() {
  const navigate = useNavigate();
  const location = useLocation();
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const [isDropdownOpen, setIsDropdownOpen] = useState(false);
  
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

  // Styles pour le logo
  const logoStyles = {
    logoContainer: {
      display: 'flex',
      alignItems: 'center',
      gap: '10px',
      cursor: 'pointer',
    },
    logoIcon: {
      position: 'relative',
      width: '40px',
      height: '40px',
    },
    square: {
      position: 'absolute',
      width: '30px',
      height: '30px',
      border: '3px solid',
      borderRadius: '5px',
      transform: 'rotate(45deg)',
    },
    squareBlue: {
      borderColor: '#2563eb',
      top: '3px',
      left: '3px',
      zIndex: 1,
    },
    squareRed: {
      borderColor: '#e63946',
      top: '8px',
      left: '8px',
      zIndex: 2,
    },
    arrow: {
      position: 'absolute',
      top: '50%',
      left: '50%',
      transform: 'translate(-50%, -50%)',
      zIndex: 3,
      width: 0,
      height: 0,
      borderLeft: '8px solid #2563eb',
      borderTop: '6px solid transparent',
      borderBottom: '6px solid transparent',
    },
    arrowBefore: {
      content: '""',
      position: 'absolute',
      top: '-3px',
      left: '-14px',
      width: '12px',
      height: '3px',
      backgroundColor: '#2563eb',
      borderRadius: '2px',
    },
    logoText: {
      display: 'flex',
      flexDirection: 'column',
      gap: '2px',
    },
    mainText: {
      fontSize: '20px',
      fontWeight: 'bold',
      color: '#e63946',
      letterSpacing: '1px',
      margin: 0,
    },
    subText: {
      fontSize: '10px',
      color: '#2563eb',
      fontWeight: '600',
      letterSpacing: '0.5px',
      margin: 0,
    },
  };

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
    logoSection: {
      display: 'flex',
      alignItems: 'center',
      gap: '20px',
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
      zIndex: 999,
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
    dropdown: {
      position: 'relative',
      display: 'inline-block',
    },
    dropdownButton: {
      backgroundColor: 'transparent',
      color: '#fff',
      border: 'none',
      padding: '10px 15px',
      borderRadius: '8px',
      cursor: 'pointer',
      fontSize: '16px',
      fontWeight: '500',
      display: 'flex',
      alignItems: 'center',
      gap: '8px',
      transition: 'all 0.3s ease',
      '&:hover': {
        backgroundColor: '#2a2638',
      },
    },
    dropdownContent: {
      position: 'absolute',
      backgroundColor: '#1f1c2c',
      minWidth: '200px',
      boxShadow: '0 8px 16px rgba(0,0,0,0.2)',
      borderRadius: '8px',
      zIndex: 1,
      top: '100%',
      left: 0,
      opacity: isDropdownOpen ? 1 : 0,
      visibility: isDropdownOpen ? 'visible' : 'hidden',
      transform: isDropdownOpen ? 'translateY(0)' : 'translateY(-10px)',
      transition: 'all 0.3s ease',
    },
    dropdownItem: {
      color: '#fff',
      padding: '12px 16px',
      textDecoration: 'none',
      display: 'flex',
      alignItems: 'center',
      gap: '8px',
      fontSize: '14px',
      '&:hover': {
        backgroundColor: '#2a2638',
      },
    },
    chevronIcon: {
      transition: 'transform 0.3s ease',
      transform: isDropdownOpen ? 'rotate(180deg)' : 'rotate(0)',
    },
  };

  return (
    <>
      <nav style={styles.navbar}>
        <div style={styles.navContent}>
          <div style={styles.logoSection}>
            {/* Logo personnalisé */}
            <div 
              style={logoStyles.logoContainer}
              onClick={() => navigate('/')}
            >
              <div style={logoStyles.logoIcon}>
                <div style={{ ...logoStyles.square, ...logoStyles.squareBlue }}></div>
                <div style={{ ...logoStyles.square, ...logoStyles.squareRed }}></div>
                <div style={logoStyles.arrow}>
                  <div style={logoStyles.arrowBefore}></div>
                </div>
              </div>
              <div style={logoStyles.logoText}>
                <h1 style={logoStyles.mainText}>JOBAI</h1>
                <p style={logoStyles.subText}>SWIPE UR JOB</p>
              </div>
            </div>
            
            {/* Dropdown Menu */}
            <div style={styles.dropdown}>
              <button 
                style={styles.dropdownButton}
                onClick={() => setIsDropdownOpen(!isDropdownOpen)}
                onMouseEnter={() => setIsDropdownOpen(true)}
                onMouseLeave={() => setIsDropdownOpen(false)}
              >
                <span style={styles.chevronIcon}>▼</span>
              </button>
              <div 
                style={styles.dropdownContent}
                onMouseEnter={() => setIsDropdownOpen(true)}
                onMouseLeave={() => setIsDropdownOpen(false)}
              >
                {menuItems.map((item) => (
                  <a
                    key={item.path}
                    href="#"
                    onClick={(e) => {
                      e.preventDefault();
                      navigate(item.path);
                      setIsDropdownOpen(false);
                    }}
                    style={{
                      ...styles.dropdownItem,
                      ...(location.pathname === item.path ? { backgroundColor: '#e63946' } : {}),
                    }}
                  >
                    <span>{item.icon}</span>
                    {item.label}
                  </a>
                ))}
              </div>
            </div>
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