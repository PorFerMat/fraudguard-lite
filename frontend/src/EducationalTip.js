import React, { useState, useEffect } from 'react';

const EducationalTip = () => {
  const [tip, setTip] = useState({ tip: '', category: '' });
  const [loading, setLoading] = useState(true);

  // Fetch a new tip from the backend
  const fetchTip = async () => {
    try {
      const response = await fetch('http://localhost:5000/api/educational-tip');
      const data = await response.json();
      setTip(data);
    } catch (error) {
      console.error('Error fetching tip:', error);
      // Fallback tip in case API is not reachable
      setTip({
        tip: 'Always verify the URL of websites before entering personal information.',
        category: 'Security'
      });
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchTip();
  }, []);

  return (
    <div className="educational-tip">
      <h3>🔒 Security Tip of the Moment</h3>
      {loading ? (
        <p>Loading tip...</p>
      ) : (
        <div className="tip-card">
          <span className="tip-category">{tip.category}</span>
          <p className="tip-text">"{tip.tip}"</p>
          <button 
            className="new-tip-btn"
            onClick={fetchTip}
          >
            Get Another Tip
          </button>
        </div>
      )}
    </div>
  );
};

export default EducationalTip;