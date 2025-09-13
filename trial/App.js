
import React, { useState } from 'react';
import './App.css';
import VideoUpload from './components/VideoUpload';
import SummaryDisplay from './components/SummaryDisplay';
import UserPreferences from './components/UserPreferences';

function App() {
  const [currentStep, setCurrentStep] = useState(1);
  const [uploadedVideo, setUploadedVideo] = useState(null);
  const [userPreferences, setUserPreferences] = useState({
    length: 'medium',
    style: 'bullet_points',
    focus: ['key_points']
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
      const response = await fetch('http://localhost:5000/process', {
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
        <h1>AI Video Summarizer</h1>
        <p>Upload a video and get an intelligent summary combining audio and visual analysis</p>
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
            <span className="step-label">Set Preferences</span>
          </div>
          <div className={`step ${currentStep >= 3 ? 'active' : ''}`}>
            <span className="step-number">3</span>
            <span className="step-label">View Summary</span>
          </div>
        </div>

        {/* Step Content */}
        {currentStep === 1 && (
          <VideoUpload onVideoUpload={handleVideoUpload} />
        )}

        {currentStep === 2 && (
          <UserPreferences 
            onPreferencesSet={handlePreferencesSet}
            currentPreferences={userPreferences}
          />
        )}

        {currentStep === 3 && (
          <div>
            {loading ? (
              <div className="loading-container">
                <div className="spinner"></div>
                <h3>Processing your video...</h3>
                <p>This may take a few minutes depending on video length</p>
                <div className="processing-steps">
                  <div className="processing-step">📝 Extracting transcript...</div>
                  <div className="processing-step">👁️ Analyzing visual content...</div>
                  <div className="processing-step">🤖 Generating summary...</div>
                </div>
              </div>
            ) : (
              summaryData && (
                <SummaryDisplay 
                  summaryData={summaryData}
                  onReset={resetApp}
                />
              )
            )}
          </div>
        )}
      </main>

      <footer className="App-footer">
        <p>Powered by free AI APIs • No data stored permanently</p>
      </footer>
    </div>
  );
}

export default App;
