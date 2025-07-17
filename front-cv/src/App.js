// src/App.js
import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Login from './Login';
import Upload from './Upload';
import Swipe from "./Swipe";
import Historique from './Historique';
import Review from "./Review";
import Home from "./Home";
import CVViewer from "./CVViewer";
import ProtectedRoute from './ProtectedRoute';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/login" element={<Login />} />
        <Route path="/upload" element={
          <ProtectedRoute>
            <Upload />
          </ProtectedRoute>
        } />
        <Route path="/swipe" element={
          <ProtectedRoute>
            <Swipe />
          </ProtectedRoute>
        } />
        <Route path="/historique" element={
          <ProtectedRoute>
            <Historique />
          </ProtectedRoute>
        } />
        <Route path="/review" element={
          <ProtectedRoute>
            <Review />
          </ProtectedRoute>
        } />
        <Route path="/cv" element={
          <ProtectedRoute>
            <CVViewer />
          </ProtectedRoute>
        } />
      </Routes>
    </Router>
  );
}

export default App;