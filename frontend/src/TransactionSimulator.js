import React, { useState } from 'react';

const TransactionSimulator = () => {
  const [simulationType, setSimulationType] = useState('legitimate');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const runSimulation = async () => {
    setLoading(true);
    setResult(null);
    
    // Mock transaction data based on simulation type
    const transactionData = {
      user_id: 'sarah123',
      amount: simulationType === 'fraudulent' ? 500 : 85,
      device: simulationType === 'fraudulent' ? 'Unknown_Device' : 'iPhone',
      typing_speed: simulationType === 'fraudulent' ? 250 : 80,
      timestamp: new Date().toISOString()
    };

    try {
      const response = await fetch('http://localhost:5000/api/risk-score', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(transactionData),
      });
      
      const data = await response.json();
      setResult(data);
    } catch (error) {
      console.error('Error running simulation:', error);
      setResult({
        risk_score: 95,
        status: 'ERROR',
        reasons: ['Unable to connect to risk service']
      });
    }
    
    setLoading(false);
  };

  return (
    <div className="simulator">
      <h3>🎭 Fraud Simulation</h3>
      
      <div className="simulation-options">
        <label>
          <input
            type="radio"
            value="legitimate"
            checked={simulationType === 'legitimate'}
            onChange={(e) => setSimulationType(e.target.value)}
          />
          Legitimate Transaction
        </label>
        
        <label>
          <input
            type="radio"
            value="fraudulent"
            checked={simulationType === 'fraudulent'}
            onChange={(e) => setSimulationType(e.target.value)}
          />
          Fraudulent Attempt
        </label>
      </div>
      
      <button 
        className="simulate-btn"
        onClick={runSimulation}
        disabled={loading}
      >
        {loading ? 'Analyzing...' : 'Run Simulation'}
      </button>
      
      {result && (
        <div className={`result result-${result.color}`}>
          <h4>Analysis Result: {result.status}</h4>
          <div className="risk-score-display">
            Risk Score: <strong>{result.risk_score}/100</strong>
          </div>
          {result.reasons.length > 0 && (
            <div className="reasons">
              <h5>🚩 Risk Factors Detected:</h5>
              <ul>
                {result.reasons.map((reason, index) => (
                  <li key={index}>{reason}</li>
                ))}
              </ul>
            </div>
          )}
        </div>
      )}
      
      <div className="simulation-description">
        <p>
          <strong>Demo Scenario:</strong><br/>
          {simulationType === 'legitimate' 
            ? "Sarah logs in from her usual iPhone and buys $85 of groceries during her normal shopping hours." 
            : "A hacker with stolen credentials tries to buy $500 in gift cards from an unknown device at 3 AM with unusually fast typing."}
        </p>
      </div>
    </div>
  );
};

export default TransactionSimulator;