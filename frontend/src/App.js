import React, { useState, useEffect } from 'react';
import Dashboard from './Dashboard';
import TransactionSimulator from './TransactionSimulator';
import EducationalTip from './EducationalTip';
import './styles/App.css';

function App() {
  const [currentRisk, setCurrentRisk] = useState(15);
  const [transactions, setTransactions] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Fetch initial data
    fetchTransactions();
    
    // Simulate real-time updates every 30 seconds
    const interval = setInterval(fetchTransactions, 30000);
    
    return () => clearInterval(interval);
  }, []);

  const fetchTransactions = async () => {
    try {
      // This URL should match your Flask backend
      const response = await fetch('http://localhost:5000/api/transactions');
      const data = await response.json();
      setTransactions(data.transactions);
      setLoading(false);
    } catch (error) {
      console.error('Error fetching transactions:', error);
      // Fallback to mock data if backend is not ready
      const mockTransactions = [
        { id: 1, amount: 85, merchant: 'Amazon', timestamp: '2024-01-15 14:30:00', risk_score: 12, status: 'APPROVED' },
        { id: 2, amount: 45, merchant: 'Starbucks', timestamp: '2024-01-15 15:45:00', risk_score: 8, status: 'APPROVED' },
        { id: 3, amount: 500, merchant: 'Unknown', timestamp: '2024-01-15 03:20:00', risk_score: 92, status: 'BLOCKED' },
      ];
      setTransactions(mockTransactions);
      setLoading(false);
    }
  };

  const handleReportFraud = (transactionId) => {
    alert(`Transaction ${transactionId} reported as fraudulent. Our AI will learn from this!`);
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>🛡️ FraudGuard Lite</h1>
        <p>AI-Powered Fraud Detection System</p>
      </header>
      
      <div className="container">
        <div className="main-dashboard">
          <Dashboard 
            currentRisk={currentRisk} 
            transactions={transactions} 
            onReportFraud={handleReportFraud}
            loading={loading}
          />
        </div>
        
        <div className="side-panel">
          <TransactionSimulator />
          <EducationalTip />
        </div>
      </div>
      
      <footer>
        <p>Built for the Digital Fraud Hackathon | {new Date().getFullYear()}</p>
      </footer>
    </div>
  );
}

export default App;