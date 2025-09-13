
import React, { useState } from 'react';

const VisualPreferences = ({ onPreferencesSet, currentPreferences }) => {
  const [preferences, setPreferences] = useState(currentPreferences);

  const handleLengthChange = (length) => {
    setPreferences(prev => ({ ...prev, length }));
  };

  const handleStyleChange = (style) => {
    setPreferences(prev => ({ ...prev, style }));
  };

  const handleDetailLevelChange = (detail_level) => {
    setPreferences(prev => ({ ...prev, detail_level: parseInt(detail_level) }));
  };

  const handleFocusChange = (focusArea) => {
    setPreferences(prev => {
      const newFocus = prev.focus.includes(focusArea)
        ? prev.focus.filter(f => f !== focusArea)
        : [...prev.focus, focusArea];
      return { ...prev, focus: newFocus };
    });
  };

  const handleSubmit = () => {
    if (preferences.focus.length === 0) {
      alert('Please select at least one focus area');
      return;
    }
    onPreferencesSet(preferences);
  };

  return (
    <div className="preferences-container">
      <h2>🎬 Customize Your Visual Analysis</h2>
      <p>Tell us what aspects of the video you want to analyze:</p>

      {/* Analysis Detail Level */}
      <div className="preference-section">
        <h3>🔍 Analysis Detail Level</h3>
        <div className="slider-container">
          <label>Number of frames to analyze: <strong>{preferences.detail_level}</strong></label>
          <input
            type="range"
            min="5"
            max="30"
            value={preferences.detail_level}
            onChange={(e) => handleDetailLevelChange(e.target.value)}
            className="detail-slider"
          />
          <div className="slider-labels">
            <span>Quick (5)</span>
            <span>Balanced (15)</span>
            <span>Thorough (30)</span>
          </div>
        </div>
        <p className="detail-description">
          More frames = more detailed analysis but longer processing time
        </p>
      </div>

      {/* Summary Length */}
      <div className="preference-section">
        <h3>📏 Summary Length</h3>
        <div className="option-group">
          {[
            { value: 'short', label: 'Concise', desc: '~150 words - Key highlights only' },
            { value: 'medium', label: 'Balanced', desc: '~300 words - Comprehensive overview' },
            { value: 'long', label: 'Detailed', desc: '~500 words - In-depth analysis' }
          ].map(option => (
            <div 
              key={option.value}
              className={`option-card ${preferences.length === option.value ? 'selected' : ''}`}
              onClick={() => handleLengthChange(option.value)}
            >
              <h4>{option.label}</h4>
              <p>{option.desc}</p>
            </div>
          ))}
        </div>
      </div>

      {/* Summary Style */}
      <div className="preference-section">
        <h3>📝 Output Format</h3>
        <div className="option-group">
          {[
            { value: 'paragraph', label: 'Narrative', desc: 'Flowing descriptive text' },
            { value: 'bullet_points', label: 'Bullet Points', desc: 'Organized key findings' },
            { value: 'numbered_list', label: 'Numbered List', desc: 'Sequential breakdown' },
            { value: 'technical_report', label: 'Technical Report', desc: 'Formal analysis document' }
          ].map(option => (
            <div 
              key={option.value}
              className={`option-card ${preferences.style === option.value ? 'selected' : ''}`}
              onClick={() => handleStyleChange(option.value)}
            >
              <h4>{option.label}</h4>
              <p>{option.desc}</p>
            </div>
          ))}
        </div>
      </div>

      {/* Visual Focus Areas */}
      <div className="preference-section">
        <h3>🎯 Visual Analysis Focus (Select multiple)</h3>
        <div className="checkbox-group">
          {[
            { value: 'visual_elements', label: 'General Visual Elements', desc: 'Overall scene types, objects, and composition' },
            { value: 'scene_analysis', label: 'Scene Classification', desc: 'Detailed breakdown of different scene types' },
            { value: 'color_analysis', label: 'Color & Lighting', desc: 'Color schemes, brightness, and visual tone' },
            { value: 'motion_analysis', label: 'Activity & Motion', desc: 'Movement detection and activity levels' },
            { value: 'visual_quality', label: 'Technical Quality', desc: 'Sharpness, exposure, and overall video quality' },
            { value: 'composition', label: 'Visual Composition', desc: 'Framing, balance, and artistic elements' },
            { value: 'key_moments', label: 'Key Visual Moments', desc: 'Important timestamps and scene changes' }
          ].map(option => (
            <div 
              key={option.value}
              className={`checkbox-card ${preferences.focus.includes(option.value) ? 'checked' : ''}`}
              onClick={() => handleFocusChange(option.value)}
            >
              <div className="checkbox">
                {preferences.focus.includes(option.value) ? '✓' : ''}
              </div>
              <div className="checkbox-content">
                <h4>{option.label}</h4>
                <p>{option.desc}</p>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Custom Instructions */}
      <div className="preference-section">
        <h3>💬 Additional Instructions (Optional)</h3>
        <textarea
          placeholder="Any specific visual elements you want to focus on? e.g., 'Focus on people and faces' or 'Analyze architectural elements'"
          value={preferences.customInstructions || ''}
          onChange={(e) => setPreferences(prev => ({ ...prev, customInstructions: e.target.value }))}
          rows={3}
          className="custom-instructions"
        />
      </div>

      <div className="preferences-actions">
        <button 
          className="btn btn-primary"
          onClick={handleSubmit}
        >
          🎬 Start Visual Analysis
        </button>
      </div>
    </div>
  );
};

export default VisualPreferences;
