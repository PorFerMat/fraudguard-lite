import React from 'react';

const RiskIndicator = ({ score }) => {
  // Determine color and label based on score
  const getRiskLevel = (score) => {
    if (score < 30) return { color: '#52c41a', label: 'Low', emoji: '✅' };
    if (score < 70) return { color: '#faad14', label: 'Medium', emoji: '⚠️' };
    return { color: '#f5222d', label: 'High', emoji: '🚨' };
  };

  const { color, label, emoji } = getRiskLevel(score);

  return (
    <div className="risk-indicator">
      <div className="risk-gauge">
        {/* Outer gauge background */}
        <div className="gauge-background">
          {/* Colored fill based on score */}
          <div 
            className="gauge-fill" 
            style={{ 
              width: `${score}%`,
              backgroundColor: color
            }}
          ></div>
        </div>
        {/* Score number displayed on top */}
        <div className="risk-score-number">
          <strong>{score}</strong>/100
        </div>
      </div>
      <div className="risk-label" style={{ color: color }}>
        {emoji} {label} Risk
      </div>
    </div>
  );
};

export default RiskIndicator;