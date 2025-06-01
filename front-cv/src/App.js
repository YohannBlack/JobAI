// src/App.js
import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Login from './Login';
import Upload from './Upload';
import Swipe from "./Swipe";

console.log("Swipe = ", Swipe);


function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Login />} />
        <Route path="/upload" element={<Upload />} />
        <Route path="/swipe" element={<Swipe />} />
      </Routes>
    </Router>
  );
}

export default App;
