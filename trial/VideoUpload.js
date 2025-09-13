
import React, { useState, useRef } from 'react';

const VideoUpload = ({ onVideoUpload }) => {
  const [selectedFile, setSelectedFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [dragActive, setDragActive] = useState(false);
  const fileInputRef = useRef(null);

  const handleFileSelect = (file) => {
    // Validate file type
    const allowedTypes = ['video/mp4', 'video/avi', 'video/mov', 'video/mkv', 'video/webm'];
    if (!allowedTypes.includes(file.type)) {
      alert('Please select a valid video file (MP4, AVI, MOV, MKV, WebM)');
      return;
    }

    // Validate file size (100MB limit)
    const maxSize = 100 * 1024 * 1024; // 100MB
    if (file.size > maxSize) {
      alert('File size must be less than 100MB');
      return;
    }

    setSelectedFile(file);
  };

  const handleUpload = async () => {
    if (!selectedFile) {
      alert('Please select a video file first');
      return;
    }

    setUploading(true);

    const formData = new FormData();
    formData.append('video', selectedFile);

    try {
      const response = await fetch('http://localhost:5000/upload', {
        method: 'POST',
        body: formData
      });

      const data = await response.json();

      if (response.ok) {
        onVideoUpload(data);
      } else {
        alert('Upload failed: ' + data.error);
      }
    } catch (error) {
      console.error('Upload error:', error);
      alert('Upload failed: ' + error.message);
    } finally {
      setUploading(false);
    }
  };

  const handleDrag = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === 'dragenter' || e.type === 'dragover') {
      setDragActive(true);
    } else if (e.type === 'dragleave') {
      setDragActive(false);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);

    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFileSelect(e.dataTransfer.files[0]);
    }
  };

  const openFileDialog = () => {
    fileInputRef.current?.click();
  };

  return (
    <div className="video-upload-container">
      <div 
        className={`upload-area ${dragActive ? 'drag-active' : ''}`}
        onDragEnter={handleDrag}
        onDragLeave={handleDrag}
        onDragOver={handleDrag}
        onDrop={handleDrop}
        onClick={openFileDialog}
      >
        <input
          ref={fileInputRef}
          type="file"
          accept="video/*"
          onChange={(e) => e.target.files[0] && handleFileSelect(e.target.files[0])}
          style={{ display: 'none' }}
        />

        {!selectedFile ? (
          <div className="upload-placeholder">
            <div className="upload-icon">📹</div>
            <h3>Upload Your Video</h3>
            <p>Drag and drop your video file here, or click to browse</p>
            <p className="file-info">Supported formats: MP4, AVI, MOV, MKV, WebM (max 100MB)</p>
          </div>
        ) : (
          <div className="file-selected">
            <div className="file-icon">✅</div>
            <h3>{selectedFile.name}</h3>
            <p>Size: {(selectedFile.size / (1024 * 1024)).toFixed(2)} MB</p>
            <p>Type: {selectedFile.type}</p>
          </div>
        )}
      </div>

      {selectedFile && (
        <div className="upload-actions">
          <button 
            className="btn btn-primary"
            onClick={handleUpload}
            disabled={uploading}
          >
            {uploading ? '⏳ Uploading...' : '🚀 Upload & Continue'}
          </button>

          <button 
            className="btn btn-secondary"
            onClick={() => setSelectedFile(null)}
            disabled={uploading}
          >
            Choose Different File
          </button>
        </div>
      )}

      <div className="upload-tips">
        <h4>💡 Tips for best results:</h4>
        <ul>
          <li>Videos with clear audio work best for transcription</li>
          <li>Good lighting helps with visual analysis</li>
          <li>Shorter videos (under 10 minutes) process faster</li>
          <li>MP4 format is recommended for compatibility</li>
        </ul>
      </div>
    </div>
  );
};

export default VideoUpload;
