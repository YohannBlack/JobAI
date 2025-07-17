// src/PDFViewer.js
import React from 'react';
import { useLocation } from 'react-router-dom';

function PDFViewer() {
  const location = useLocation();
  const query = new URLSearchParams(location.search);
  const pdfUrl = query.get('url');

  return (
    <div style={{ height: '100vh', width: '100%' }}>
      <iframe 
        src={`https://docs.google.com/gview?url=${pdfUrl}&embedded=true`}
        style={{ width: '100%', height: '100%', border: 'none' }}
        title="PDF Viewer"
      />
    </div>
  );
}

export default PDFViewer;