import React, { useState, useRef } from 'react';
import './App.css';

function App() {
  const [files, setFiles] = useState([]);
  const [loading, setLoading] = useState(false);
  const fileInputRef = useRef(null);

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    if (selectedFile) {
      setFiles((prevFiles) => [...prevFiles, selectedFile]);
    }
  };

  const removeFile = (indexToRemove) => {
    setFiles((prevFiles) => prevFiles.filter((_, index) => index !== indexToRemove));
  };

  const handleUpload = async () => {
    if (!files.length) {
      alert('Por favor selecciona al menos un archivo');
      return;
    }

    setLoading(true);

    const formData = new FormData();
    for (let file of files) {
      formData.append('files', file);
    }

    try {
      const response = await fetch('http://localhost:5000/convert_files', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        alert('Error al convertir los archivos');
        setLoading(false);
        return;
      }

      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;

      if (files.length === 1) {
        a.download = `convertido_${files[0].name}`;
      } else {
        a.download = 'archivos_convertidos_300dpi.zip';
      }

      document.body.appendChild(a);
      a.click();
      a.remove();

      // Limpiar archivos después de la descarga
      setFiles([]);

    } catch (error) {
      alert('Error de conexión al backend');
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container">
      <h1 className="title">Convertidor a 300 DPI</h1>
      <input
        type="file"
        ref={fileInputRef}
        onChange={handleFileChange}
        accept=".pdf,.jpg,.jpeg,.png,.doc,.docx"
        style={{ display: 'none' }}
      />
      <button className="button upload" onClick={() => fileInputRef.current.click()}>
        Subir archivo
      </button>
      <div className="file-list">
        {files.map((file, index) => (
          <div key={index} className="file-item">
            <span>{file.name}</span>
            <button className="remove-button" onClick={() => removeFile(index)}>X</button>
          </div>
        ))}
      </div>
      <button className="button convert" onClick={handleUpload} disabled={loading}>
        {loading ? 'Convirtiendo...' : 'Convertir a 300 DPI'}
      </button>
    </div>
  );
}

export default App;






