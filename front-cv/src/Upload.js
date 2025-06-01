import React, { useState } from "react";
import { useNavigate } from "react-router-dom"; 

function Upload() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [cvData, setCvData] = useState(null);

  const navigate = useNavigate();

  const handleFileChange = (event) => {
    setSelectedFile(event.target.files[0]);
  };

  const handleUpload = async (e) => {
    e.preventDefault();

    if (!selectedFile) {
      alert("Aucun fichier sélectionné");
      return;
    }

    const formData = new FormData();
    formData.append("file", selectedFile);

    try {
      const response = await fetch("http://localhost:5000/extract", {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        throw new Error("Erreur lors de l'extraction");
      }

      const data = await response.json();
      console.log("Réponse du backend :", data);
      setCvData(data);
    } catch (error) {
      console.error("Erreur :", error);
    }
  };

  const handleGoSwipe = () => {
    navigate("/swipe"); // <-- redirection vers la page Swipe
  };

  // Styles
  const containerStyle = {
    fontFamily: "Arial, sans-serif",
    maxWidth: "600px",
    margin: "40px auto",
    padding: "20px",
    border: "1px solid #ccc",
    borderRadius: "8px",
    boxShadow: "0 2px 8px rgba(0,0,0,0.1)",
    backgroundColor: "#f9f9f9",
  };

  const headingStyle = {
    textAlign: "center",
    color: "#333",
  };

  const inputStyle = {
    display: "block",
    margin: "20px auto",
  };

  const buttonStyle = {
    display: "block",
    margin: "10px auto",
    padding: "10px 20px",
    backgroundColor: "#4CAF50",
    color: "white",
    border: "none",
    borderRadius: "4px",
    cursor: "pointer",
  };

  const resultStyle = {
    marginTop: "30px",
    backgroundColor: "#fff",
    padding: "15px",
    borderRadius: "6px",
    border: "1px solid #ddd",
  };

  return (
    <div style={containerStyle}>
      <h1 style={headingStyle}>Bienvenue Dihia BELARBIA</h1>
      <p style={{ textAlign: "center" }}>Téléverse ton CV ici (PDF uniquement)</p>
      <input type="file" accept=".pdf" onChange={handleFileChange} style={inputStyle} />
      <button onClick={handleUpload} style={buttonStyle}>Uploader mon CV</button>

      {cvData && (
        <div style={resultStyle}>
          <h2>Informations extraites :</h2>
          <p><strong>Nom :</strong> {cvData.nom}</p>
          <p><strong>Email :</strong> {cvData.email}</p>
          <p><strong>Téléphone :</strong> {cvData.telephone}</p>
          <p><strong>Compétences :</strong> {cvData.competences}</p>
          <p><strong>Adresse :</strong> {cvData.adresse}</p>

          <button onClick={handleGoSwipe} style={{ ...buttonStyle, backgroundColor: "#2196F3" }}>
            Go Swipe
          </button>
        </div>
      )}
    </div>
  );
}

export default Upload;
