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
    
    // Simulate real-time updates
    const interval = setInterval(() => {
      fetchTransactions();
    }, 30000); // Every 30 seconds
    
    return () => clearInterval(interval);
  }, []);

  const fetchTransactions = async () => {
    try {
      const response = await fetch('http://localhost:5000/api/transactions');
      const data = await response.json();
      setTransactions(data.transactions);
      setLoading(false);
    } catch (error) {
      console.error('Error fetching transactions:', error);
    }
  };

  const handleReportFraud = (transactionId) => {
    alert(`Transaction ${transactionId} reported as fraudulent. Our AI will learn from this!`);
    // In a real app, this would send to backend
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