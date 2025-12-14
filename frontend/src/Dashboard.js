import React from 'react';
import RiskIndicator from './RiskIndicator';

const Dashboard = ({ currentRisk, transactions, onReportFraud, loading }) => {
  const getRiskColor = (score) => {
    if (score < 30) return 'green';
    if (score < 70) return 'orange';
    return 'red';
  };

  const getStatusIcon = (status) => {
    switch(status) {
      case 'APPROVED': return '✅';
      case 'BLOCKED': return '❌';
      case 'REVIEWED': return '⚠️';
      default: return '🔍';
    }
  };

  if (loading) {
    return <div className="loading">Loading dashboard data...</div>;
  }

  return (
    <div className="dashboard">
      <div className="dashboard-header">
        <h2>Live Fraud Dashboard</h2>
        <div className="risk-summary">
          <RiskIndicator score={currentRisk} />
          <p>Overall System Risk: <strong>{currentRisk}/100</strong></p>
        </div>
      </div>
      
      <div className="transactions-table">
        <h3>Recent Transactions</h3>
        <table>
          <thead>
            <tr>
              <th>Merchant</th>
              <th>Amount</th>
              <th>Time</th>
              <th>Risk Score</th>
              <th>Status</th>
              <th>Action</th>
            </tr>
          </thead>
          <tbody>
            {transactions.slice(0, 5).map((tx) => (
              <tr key={tx.id} className={`risk-${getRiskColor(tx.risk_score)}`}>
                <td>{tx.merchant}</td>
                <td>${tx.amount}</td>
                <td>{tx.timestamp.split(' ')[1]}</td>
                <td>
                  <div className="risk-bar">
                    <div 
                      className="risk-fill" 
                      style={{width: `${tx.risk_score}%`, backgroundColor: getRiskColor(tx.risk_score)}}
                    ></div>
                    <span>{tx.risk_score}</span>
                  </div>
                </td>
                <td>
                  <span className={`status-badge status-${tx.status.toLowerCase()}`}>
                    {getStatusIcon(tx.status)} {tx.status}
                  </span>
                </td>
                <td>
                  <button 
                    className="report-btn"
                    onClick={() => onReportFraud(tx.id)}
                  >
                    Report
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      
      <div className="stats-grid">
        <div className="stat-card">
          <h4>Today's Transactions</h4>
          <p className="stat-number">47</p>
        </div>
        <div className="stat-card">
          <h4>Blocked Fraud</h4>
          <p className="stat-number">3</p>
        </div>
        <div className="stat-card">
          <h4>Avg. Risk Score</h4>
          <p className="stat-number">28</p>
        </div>
        <div className="stat-card">
          <h4>AI Confidence</h4>
          <p className="stat-number">94%</p>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;