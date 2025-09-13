
import React, { useState } from 'react';

const SummaryDisplay = ({ summaryData, onReset }) => {
  const [activeTab, setActiveTab] = useState('summary');

  const handleCopyToClipboard = (text) => {
    navigator.clipboard.writeText(text).then(() => {
      alert('Copied to clipboard!');
    });
  };

  const handleDownload = (content, filename) => {
    const element = document.createElement('a');
    const file = new Blob([content], { type: 'text/plain' });
    element.href = URL.createObjectURL(file);
    element.download = filename;
    document.body.appendChild(element);
    element.click();
    document.body.removeChild(element);
  };

  const formatTimestamp = (seconds) => {
    const minutes = Math.floor(seconds / 60);
    const remainingSeconds = Math.floor(seconds % 60);
    return `${minutes}:${remainingSeconds.toString().padStart(2, '0')}`;
  };

  return (
    <div className="summary-display-container">
      <div className="summary-header">
        <h2>📋 Your Video Summary</h2>
        <div className="summary-stats">
          <span>📝 {summaryData.transcript_length} words transcribed</span>
          <span>👁️ {summaryData.visual_elements_detected} visual elements detected</span>
          <span>⏱️ Generated at {new Date(summaryData.generation_time).toLocaleTimeString()}</span>
        </div>
      </div>

      {/* Tab Navigation */}
      <div className="tab-navigation">
        <button 
          className={`tab ${activeTab === 'summary' ? 'active' : ''}`}
          onClick={() => setActiveTab('summary')}
        >
          🤖 AI Summary
        </button>
        <button 
          className={`tab ${activeTab === 'transcript' ? 'active' : ''}`}
          onClick={() => setActiveTab('transcript')}
        >
          📝 Full Transcript
        </button>
        <button 
          className={`tab ${activeTab === 'visual' ? 'active' : ''}`}
          onClick={() => setActiveTab('visual')}
        >
          👁️ Visual Analysis
        </button>
      </div>

      {/* Tab Content */}
      <div className="tab-content">
        {activeTab === 'summary' && (
          <div className="summary-tab">
            <div className="content-box">
              <div className="content-header">
                <h3>Final Summary</h3>
                <div className="action-buttons">
                  <button 
                    className="btn btn-small"
                    onClick={() => handleCopyToClipboard(summaryData.final_summary.summary)}
                  >
                    📋 Copy
                  </button>
                  <button 
                    className="btn btn-small"
                    onClick={() => handleDownload(summaryData.final_summary.summary, 'video_summary.txt')}
                  >
                    💾 Download
                  </button>
                </div>
              </div>
              <div className="summary-content">
                <pre>{summaryData.final_summary.summary}</pre>
              </div>
            </div>

            {/* User Preferences Used */}
            <div className="content-box">
              <h3>⚙️ Summary Settings Used</h3>
              <div className="preferences-display">
                <div className="pref-item">
                  <strong>Length:</strong> {summaryData.final_summary.user_preferences.length}
                </div>
                <div className="pref-item">
                  <strong>Style:</strong> {summaryData.final_summary.user_preferences.style}
                </div>
                <div className="pref-item">
                  <strong>Focus Areas:</strong> {summaryData.final_summary.user_preferences.focus.join(', ')}
                </div>
              </div>
            </div>
          </div>
        )}

        {activeTab === 'transcript' && (
          <div className="transcript-tab">
            <div className="content-box">
              <div className="content-header">
                <h3>Full Transcript</h3>
                <div className="action-buttons">
                  <button 
                    className="btn btn-small"
                    onClick={() => handleCopyToClipboard(summaryData.transcript)}
                  >
                    📋 Copy
                  </button>
                  <button 
                    className="btn btn-small"
                    onClick={() => handleDownload(summaryData.transcript, 'video_transcript.txt')}
                  >
                    💾 Download
                  </button>
                </div>
              </div>
              <div className="transcript-content">
                <p>{summaryData.transcript}</p>
              </div>
            </div>
          </div>
        )}

        {activeTab === 'visual' && (
          <div className="visual-tab">
            <div className="content-box">
              <h3>🎬 Visual Analysis Results</h3>

              {summaryData.visual_analysis.visual_summary && (
                <div className="visual-summary">
                  <h4>Overview</h4>
                  <p>{summaryData.visual_analysis.visual_summary}</p>
                </div>
              )}

              {summaryData.visual_analysis.top_visual_elements && (
                <div className="visual-elements">
                  <h4>Top Visual Elements</h4>
                  <div className="element-tags">
                    {summaryData.visual_analysis.top_visual_elements.map((element, index) => (
                      <span key={index} className="element-tag">
                        {element}
                      </span>
                    ))}
                  </div>
                </div>
              )}

              {summaryData.visual_analysis.scene_changes && (
                <div className="scene-changes">
                  <h4>Key Moments</h4>
                  <div className="timeline">
                    {summaryData.visual_analysis.scene_changes.slice(0, 5).map((scene, index) => (
                      <div key={index} className="timeline-item">
                        <div className="timestamp">
                          {formatTimestamp(scene.timestamp)}
                        </div>
                        <div className="scene-info">
                          Scene {index + 1}: Visual content detected
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              <div className="analysis-stats">
                <h4>📊 Analysis Statistics</h4>
                <div className="stats-grid">
                  <div className="stat-item">
                    <strong>Frames Analyzed:</strong> 
                    {summaryData.visual_analysis.total_frames_analyzed}
                  </div>
                  <div className="stat-item">
                    <strong>Visual Elements Found:</strong> 
                    {Object.keys(summaryData.visual_analysis.element_frequencies || {}).length}
                  </div>
                  <div className="stat-item">
                    <strong>Scene Changes:</strong> 
                    {summaryData.visual_analysis.scene_changes?.length || 0}
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Action Buttons */}
      <div className="summary-actions">
        <button 
          className="btn btn-secondary"
          onClick={onReset}
        >
          🔄 Process Another Video
        </button>

        <button 
          className="btn btn-primary"
          onClick={() => {
            const fullReport = `
AI VIDEO SUMMARY REPORT
Generated: ${new Date(summaryData.generation_time).toLocaleString()}

=== SUMMARY ===
${summaryData.final_summary.summary}

=== FULL TRANSCRIPT ===
${summaryData.transcript}

=== VISUAL ANALYSIS ===
${summaryData.visual_analysis.visual_summary || 'No visual summary available'}

Top Visual Elements: ${summaryData.visual_analysis.top_visual_elements?.join(', ') || 'None detected'}

=== PROCESSING DETAILS ===
Transcript Length: ${summaryData.transcript_length} words
Visual Elements Detected: ${summaryData.visual_elements_detected}
Preferences Used: Length=${summaryData.final_summary.user_preferences.length}, Style=${summaryData.final_summary.user_preferences.style}, Focus=${summaryData.final_summary.user_preferences.focus.join(', ')}
            `.trim();

            handleDownload(fullReport, 'complete_video_analysis.txt');
          }}
        >
          📄 Download Full Report
        </button>
      </div>
    </div>
  );
};

export default SummaryDisplay;
