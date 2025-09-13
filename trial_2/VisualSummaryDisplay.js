
import React, { useState } from 'react';

const VisualSummaryDisplay = ({ summaryData, onReset }) => {
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
        <h2>🎬 Visual Analysis Results</h2>
        <div className="summary-stats">
          <span>📹 {summaryData.frames_analyzed} frames analyzed</span>
          <span>🎨 {summaryData.final_summary.visual_elements_detected} visual elements detected</span>
          <span>⏱️ Generated at {new Date(summaryData.final_summary.generation_time).toLocaleTimeString()}</span>
        </div>
      </div>

      {/* Tab Navigation */}
      <div className="tab-navigation">
        <button 
          className={`tab ${activeTab === 'summary' ? 'active' : ''}`}
          onClick={() => setActiveTab('summary')}
        >
          📋 Visual Summary
        </button>
        <button 
          className={`tab ${activeTab === 'analysis' ? 'active' : ''}`}
          onClick={() => setActiveTab('analysis')}
        >
          📊 Detailed Analysis
        </button>
        <button 
          className={`tab ${activeTab === 'timeline' ? 'active' : ''}`}
          onClick={() => setActiveTab('timeline')}
        >
          ⏰ Visual Timeline
        </button>
        <button 
          className={`tab ${activeTab === 'stats' ? 'active' : ''}`}
          onClick={() => setActiveTab('stats')}
        >
          📈 Statistics
        </button>
      </div>

      {/* Tab Content */}
      <div className="tab-content">
        {activeTab === 'summary' && (
          <div className="summary-tab">
            <div className="content-box">
              <div className="content-header">
                <h3>🎬 Visual Analysis Summary</h3>
                <div className="action-buttons">
                  <button 
                    className="btn btn-small"
                    onClick={() => handleCopyToClipboard(summaryData.final_summary.summary)}
                  >
                    📋 Copy
                  </button>
                  <button 
                    className="btn btn-small"
                    onClick={() => handleDownload(summaryData.final_summary.summary, 'visual_summary.txt')}
                  >
                    💾 Download
                  </button>
                </div>
              </div>
              <div className="summary-content">
                <pre>{summaryData.final_summary.summary}</pre>
              </div>
            </div>

            {/* Processing Settings */}
            <div className="content-box">
              <h3>⚙️ Analysis Settings Used</h3>
              <div className="preferences-display">
                <div className="pref-item">
                  <strong>Summary Length:</strong> {summaryData.final_summary.user_preferences.length}
                </div>
                <div className="pref-item">
                  <strong>Output Style:</strong> {summaryData.final_summary.user_preferences.style}
                </div>
                <div className="pref-item">
                  <strong>Detail Level:</strong> {summaryData.final_summary.user_preferences.detail_level} frames
                </div>
                <div className="pref-item">
                  <strong>Focus Areas:</strong> {summaryData.final_summary.user_preferences.focus.join(', ')}
                </div>
              </div>
            </div>
          </div>
        )}

        {activeTab === 'analysis' && (
          <div className="analysis-tab">
            <div className="content-box">
              <h3>🎨 Video Characteristics</h3>

              {summaryData.visual_analysis.video_characteristics && (
                <div className="characteristics-grid">
                  <div className="char-section">
                    <h4>Scene Types</h4>
                    <div className="tags">
                      {Object.entries(summaryData.visual_analysis.video_characteristics.dominant_scene_types || {}).map(([type, count]) => (
                        <span key={type} className="tag scene-tag">
                          {type}: {count}
                        </span>
                      ))}
                    </div>
                  </div>

                  <div className="char-section">
                    <h4>Activity Levels</h4>
                    <div className="tags">
                      {Object.entries(summaryData.visual_analysis.video_characteristics.activity_levels || {}).map(([level, count]) => (
                        <span key={level} className="tag activity-tag">
                          {level}: {count}
                        </span>
                      ))}
                    </div>
                  </div>

                  <div className="char-section">
                    <h4>Color Schemes</h4>
                    <div className="tags">
                      {Object.entries(summaryData.visual_analysis.video_characteristics.color_schemes || {}).map(([scheme, count]) => (
                        <span key={scheme} className="tag color-tag">
                          {scheme.replace('_', ' ')}: {count}
                        </span>
                      ))}
                    </div>
                  </div>

                  <div className="char-section">
                    <h4>Quality Assessment</h4>
                    <div className="quality-display">
                      <div className="quality-score">
                        {summaryData.visual_analysis.video_characteristics.average_quality_score?.toFixed(1) || 'N/A'}/100
                      </div>
                      <div className="quality-bar">
                        <div 
                          className="quality-fill" 
                          style={{width: `${summaryData.visual_analysis.video_characteristics.average_quality_score || 0}%`}}
                        ></div>
                      </div>
                    </div>
                  </div>
                </div>
              )}
            </div>

            {summaryData.visual_analysis.key_moments && (
              <div className="content-box">
                <h3>⭐ Key Visual Moments</h3>
                <div className="key-moments">
                  {summaryData.visual_analysis.key_moments.map((moment, index) => (
                    <div key={index} className="moment-card">
                      <div className="moment-time">{moment.timestamp_formatted}</div>
                      <div className="moment-details">
                        <div className="moment-type">{moment.scene_type}</div>
                        <div className="moment-activity">Activity: {moment.activity_level}</div>
                        {moment.has_text && <div className="moment-badge">📝 Text detected</div>}
                        {moment.frame_type === 'scene_change' && <div className="moment-badge">🔄 Scene change</div>}
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        )}

        {activeTab === 'timeline' && (
          <div className="timeline-tab">
            <div className="content-box">
              <h3>⏰ Visual Timeline</h3>
              <div className="timeline-container">
                {summaryData.visual_analysis.timeline_analysis?.map((event, index) => (
                  <div key={index} className="timeline-event">
                    <div className="timeline-marker">
                      <div className="timestamp">{event.timestamp_formatted}</div>
                    </div>
                    <div className="timeline-content">
                      <div className="event-scene">{event.scene_type}</div>
                      <div className="event-details">
                        <span className={`activity-badge ${event.activity_level}`}>
                          {event.activity_level} activity
                        </span>
                        <span className={`quality-badge ${event.quality_rating}`}>
                          {event.quality_rating} quality
                        </span>
                        {event.has_text && <span className="text-badge">📝 Text</span>}
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}

        {activeTab === 'stats' && (
          <div className="stats-tab">
            <div className="content-box">
              <h3>📊 Analysis Statistics</h3>
              <div className="stats-grid">
                <div className="stat-card">
                  <div className="stat-number">{summaryData.frames_analyzed}</div>
                  <div className="stat-label">Frames Analyzed</div>
                </div>
                <div className="stat-card">
                  <div className="stat-number">{summaryData.final_summary.visual_elements_detected}</div>
                  <div className="stat-label">Visual Elements</div>
                </div>
                <div className="stat-card">
                  <div className="stat-number">{summaryData.final_summary.key_moments_identified}</div>
                  <div className="stat-label">Key Moments</div>
                </div>
                <div className="stat-card">
                  <div className="stat-number">{summaryData.visual_analysis.scene_changes?.length || 0}</div>
                  <div className="stat-label">Scene Changes</div>
                </div>
              </div>

              {summaryData.visual_analysis.video_characteristics?.text_presence && (
                <div className="text-analysis">
                  <h4>📝 Text Detection</h4>
                  <p>Text content detected in video at timestamps:</p>
                  <div className="text-timestamps">
                    {summaryData.visual_analysis.video_characteristics.text_timestamps?.map((timestamp, index) => (
                      <span key={index} className="timestamp-badge">
                        {formatTimestamp(timestamp)}
                      </span>
                    ))}
                  </div>
                </div>
              )}
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
          🔄 Analyze Another Video
        </button>

        <button 
          className="btn btn-primary"
          onClick={() => {
            const fullReport = `
VISUAL ANALYSIS REPORT
Generated: ${new Date(summaryData.final_summary.generation_time).toLocaleString()}

=== VISUAL SUMMARY ===
${summaryData.final_summary.summary}

=== ANALYSIS DETAILS ===
Frames Analyzed: ${summaryData.frames_analyzed}
Visual Elements Detected: ${summaryData.final_summary.visual_elements_detected}
Key Moments: ${summaryData.final_summary.key_moments_identified}
Processing Mode: ${summaryData.processing_mode}

=== SETTINGS USED ===
Detail Level: ${summaryData.final_summary.user_preferences.detail_level} frames
Summary Length: ${summaryData.final_summary.user_preferences.length}
Output Style: ${summaryData.final_summary.user_preferences.style}
Focus Areas: ${summaryData.final_summary.user_preferences.focus.join(', ')}

=== VIDEO CHARACTERISTICS ===
${JSON.stringify(summaryData.final_summary.video_characteristics, null, 2)}
            `.trim();

            handleDownload(fullReport, 'complete_visual_analysis.txt');
          }}
        >
          📄 Download Full Report
        </button>
      </div>
    </div>
  );
};

export default VisualSummaryDisplay;
