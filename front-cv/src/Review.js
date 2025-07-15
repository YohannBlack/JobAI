import React, { useEffect, useState } from "react";
import { useNavigate, useLocation } from "react-router-dom";

function Review() {
  const navigate = useNavigate();
  const location = useLocation();
  const [cvData, setCvData] = useState(location.state?.cvData || null);

  useEffect(() => {
    if (!cvData) {
      navigate("/upload"); // sécurité : si pas de données, redirection
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
  try {
    const response = await fetch("https://172.189.14.214/update-profile", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        entities: cvData.entities,
        blob_filename: cvData.blob_filename,
      }),
      mode: "cors",
    });

    if (!response.ok) {
      throw new Error("Erreur lors de la mise à jour du profil");
    }

    navigate("/swipe");
  } catch (error) {
    console.error("Erreur :", error);
  }
};

  const styles = {
    container: {
      padding: "30px",
      maxWidth: "800px",
      margin: "0 auto",
      fontFamily: "Arial, sans-serif",
    },
    title: {
      fontSize: "24px",
      marginBottom: "20px",
    },
    entityBlock: {
      marginBottom: "15px",
    },
    label: {
      display: "block",
      fontWeight: "bold",
      marginBottom: "5px",
    },
    input: {
      width: "100%",
      padding: "10px",
      borderRadius: "6px",
      border: "1px solid #ccc",
    },
    summaryBlock: {
      marginTop: "30px",
      backgroundColor: "#f9f9f9",
      padding: "20px",
      borderRadius: "10px",
    },
    button: {
      padding: "12px 20px",
      backgroundColor: "#2196F3",
      color: "#fff",
      border: "none",
      borderRadius: "8px",
      cursor: "pointer",
      marginTop: "20px",
      fontWeight: "bold",
    },
  };

  return (
    <div style={styles.container}>
      <h1 style={styles.title}>Vérification des entités extraites</h1>

      <div style={styles.entityBlock}>
  <label style={styles.label}>Nom Prénom</label>
  <input
    type="text"
    value={cvData.entities.find(e => e.label === "PER")?.text || ""}
    onChange={(e) => handleEntityChange("PER", e.target.value)}
    style={styles.input}
  />
</div>

<div style={styles.entityBlock}>
  <label style={styles.label}>Ville</label>
  <input
    type="text"
    value={cvData.entities.find(e => e.label === "LOC")?.text || ""}
    onChange={(e) => handleEntityChange("LOC", e.target.value)}
    style={styles.input}
  />
</div>

<div style={styles.entityBlock}>
  <label style={styles.label}>Email</label>
  <input
    type="email"
    value={cvData.entities.find(e => e.label === "EMAIL")?.text || ""}
    onChange={(e) => handleEntityChange("EMAIL", e.target.value)}
    style={styles.input}
  />
</div>

<div style={styles.entityBlock}>
  <label style={styles.label}>Téléphone</label>
  <input
    type="tel"
    value={cvData.entities.find(e => e.label === "PHONE")?.text || ""}
    onChange={(e) => handleEntityChange("PHONE", e.target.value)}
    style={styles.input}
  />
</div>

<div style={styles.entityBlock}>
  <label style={styles.label}>Compétences</label>
  <ul style={{ paddingLeft: "20px", marginTop: "4px" }}>
    {cvData.entities
      .filter(e => e.label === "MISC")
      .map((skill, index) => (
        <li key={index}>{skill.text}</li>
      ))}
  </ul>
</div>
      {/*cvData?.summary && (
        <div style={styles.summaryBlock}>
          <h2>🧠 Résumé :</h2>
          <p>{cvData.summary}</p>
        </div>
      )*/}

      <button onClick={handleGoSwipe} style={styles.button}>Go Swipe</button>
    </div>
  );
}

export default Review;
