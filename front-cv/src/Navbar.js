import React from "react";
import { Link } from "react-router-dom";

function Navbar() {
  const styles = {
    nav: {
      backgroundColor: "#1976D2",
      padding: "15px 30px",
      display: "flex",
      justifyContent: "space-between",
      alignItems: "center",
    },
    title: {
      color: "white",
      fontSize: "20px",
      fontWeight: "bold",
      textDecoration: "none",
    },
    links: {
      display: "flex",
      gap: "20px",
    },
    link: {
      color: "white",
      textDecoration: "none",
      fontWeight: "bold",
    },
  };

  return (
    <nav style={styles.nav}>
      <Link to="/home" style={styles.title}>JobAI</Link>
      <div style={styles.links}>
        <Link to="/history" style={styles.link}>Historique</Link>
        <Link to="/cv" style={styles.link}>Mon CV</Link>
        <Link to="/review" style={styles.link}>Entités</Link>
      </div>
    </nav>
  );
}

export default Navbar;
