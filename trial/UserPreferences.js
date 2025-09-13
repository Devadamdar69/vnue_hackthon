
import React, { useState } from 'react';

const UserPreferences = ({ onPreferencesSet, currentPreferences }) => {
  const [preferences, setPreferences] = useState(currentPreferences);

  const handleLengthChange = (length) => {
    setPreferences(prev => ({ ...prev, length }));
  };

  const handleStyleChange = (style) => {
    setPreferences(prev => ({ ...prev, style }));
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
      <h2>Customize Your Summary</h2>
      <p>Tell us what kind of summary you want:</p>

      {/* Summary Length */}
      <div className="preference-section">
        <h3>📏 Summary Length</h3>
        <div className="option-group">
          {[
            { value: 'short', label: 'Short', desc: '~100 words - Quick overview' },
            { value: 'medium', label: 'Medium', desc: '~200 words - Balanced detail' },
            { value: 'long', label: 'Long', desc: '~400 words - Comprehensive' }
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
        <h3>📝 Summary Style</h3>
        <div className="option-group">
          {[
            { value: 'paragraph', label: 'Paragraph', desc: 'Flowing narrative text' },
            { value: 'bullet_points', label: 'Bullet Points', desc: 'Clear, organized points' },
            { value: 'numbered_list', label: 'Numbered List', desc: 'Sequential ordered list' }
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

      {/* Focus Areas */}
      <div className="preference-section">
        <h3>🎯 Focus Areas (Select multiple)</h3>
        <div className="checkbox-group">
          {[
            { value: 'key_points', label: 'Key Points', desc: 'Main topics and important information' },
            { value: 'visual_elements', label: 'Visual Content', desc: 'What was shown in the video' },
            { value: 'timestamps', label: 'Key Moments', desc: 'Important timestamps and scene changes' },
            { value: 'action_items', label: 'Action Items', desc: 'Tasks and next steps mentioned' },
            { value: 'statistics', label: 'Numbers & Stats', desc: 'Quantitative information' }
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
          placeholder="Any specific instructions for your summary? e.g., 'Focus on technical details' or 'Summarize for a general audience'"
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
          🤖 Generate Summary
        </button>
      </div>
    </div>
  );
};

export default UserPreferences;
