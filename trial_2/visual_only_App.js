
import React, { useState } from 'react';
import './App.css';
import VideoUpload from './components/VideoUpload';
import VisualSummaryDisplay from './components/VisualSummaryDisplay';
import VisualPreferences from './components/VisualPreferences';

function App() {
  const [currentStep, setCurrentStep] = useState(1);
  const [uploadedVideo, setUploadedVideo] = useState(null);
  const [userPreferences, setUserPreferences] = useState({
    length: 'medium',
    style: 'bullet_points',
    focus: ['visual_elements'],
    detail_level: 15
  });
  const [summaryData, setSummaryData] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleVideoUpload = (videoData) => {
    setUploadedVideo(videoData);
    setCurrentStep(2);
  };

  const handlePreferencesSet = (preferences) => {
    setUserPreferences(preferences);
    setCurrentStep(3);
    processVideo(preferences);
  };

  const processVideo = async (preferences) => {
    setLoading(true);

    try {
      const response = await fetch('http://localhost:5000/process-visual', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          filepath: uploadedVideo.filepath,
          preferences: preferences
        })
      });

      const data = await response.json();

      if (data.success) {
        setSummaryData(data);
      } else {
        console.error('Processing failed:', data.error);
        alert('Processing failed: ' + data.error);
      }
    } catch (error) {
      console.error('Error processing video:', error);
      alert('Error processing video: ' + error.message);
    } finally {
      setLoading(false);
    }
  };

  const resetApp = () => {
    setCurrentStep(1);
    setUploadedVideo(null);
    setSummaryData(null);
    setLoading(false);
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>🎬 AI Visual Video Analyzer</h1>
        <p>Upload a video and get intelligent visual analysis - No audio processing needed!</p>
        <div className="mode-indicator">
          <span className="mode-badge">👁️ Visual-Only Mode</span>
        </div>
      </header>

      <main className="App-main">
        {/* Progress Indicator */}
        <div className="progress-indicator">
          <div className={`step ${currentStep >= 1 ? 'active' : ''}`}>
            <span className="step-number">1</span>
            <span className="step-label">Upload Video</span>
          </div>
          <div className={`step ${currentStep >= 2 ? 'active' : ''}`}>
            <span className="step-number">2</span>
            <span className="step-label">Visual Preferences</span>
          </div>
          <div className={`step ${currentStep >= 3 ? 'active' : ''}`}>
            <span className="step-number">3</span>
            <span className="step-label">Visual Analysis</span>
          </div>
        </div>

        {/* Step Content */}
        {currentStep === 1 && (
          <VideoUpload onVideoUpload={handleVideoUpload} visualOnly={true} />
        )}

        {currentStep === 2 && (
          <VisualPreferences 
            onPreferencesSet={handlePreferencesSet}
            currentPreferences={userPreferences}
          />
        )}

        {currentStep === 3 && (
          <div>
            {loading ? (
              <div className="loading-container">
                <div className="spinner"></div>
                <h3>Analyzing your video visually...</h3>
                <p>Processing frames and detecting visual patterns</p>
                <div className="processing-steps">
                  <div className="processing-step">📹 Extracting key frames...</div>
                  <div className="processing-step">🎨 Analyzing colors and composition...</div>
                  <div className="processing-step">🏃 Detecting activity and motion...</div>
                  <div className="processing-step">📊 Assessing visual quality...</div>
                  <div className="processing-step">📝 Generating visual summary...</div>
                </div>
              </div>
            ) : (
              summaryData && (
                <VisualSummaryDisplay 
                  summaryData={summaryData}
                  onReset={resetApp}
                />
              )
            )}
          </div>
        )}
      </main>

      <footer className="App-footer">
        <p>👁️ Visual-Only Analysis • 🆓 No audio processing • 🔒 Privacy-focused</p>
      </footer>
    </div>
  );
}

export default App;
