from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from datetime import datetime
import random
import json
import os
from synthetic_data import generate_transaction_history

app = Flask(__name__)
CORS(app)  # Enable CORS for React frontend

# Mock user database (in real app, use a real DB)
users = {
    "sarah123": {"normal_hours": [9, 21], "avg_amount": 85.0, "usual_device": "iPhone"},
    "john_doe": {"normal_hours": [18, 23], "avg_amount": 120.0, "usual_device": "Windows_PC"}
}

def calculate_risk_score(user_id, transaction_data):
    """Calculate risk score based on transaction behavior"""
    risk_score = 0
    reasons = []
    
    if user_id not in users:
        risk_score += 40
        reasons.append("Unknown user profile")
        user_profile = {"normal_hours": [9, 17], "avg_amount": 100.0}
    else:
        user_profile = users[user_id]
    
    # 1. Time anomaly check (30 points max)
    current_hour = datetime.now().hour
    normal_start, normal_end = user_profile["normal_hours"]
    
    if not (normal_start <= current_hour <= normal_end):
        time_risk = min(30, abs(current_hour - normal_start) * 3)
        risk_score += time_risk
        reasons.append(f"Transaction outside normal hours (user usually shops between {normal_start}:00-{normal_end}:00)")
    
    # 2. Amount anomaly (40 points max)
    amount = transaction_data.get("amount", 0)
    avg_amount = user_profile.get("avg_amount", 100)
    
    if amount > avg_amount * 2:
        amount_risk = min(40, (amount / avg_amount) * 10)
        risk_score += amount_risk
        reasons.append(f"Amount (${amount}) is significantly higher than average (${avg_amount})")
    
    # 3. Device check (20 points max)
    device = transaction_data.get("device", "unknown")
    usual_device = user_profile.get("usual_device", "")
    
    if device != usual_device and usual_device:
        risk_score += 20
        reasons.append(f"New device detected: {device} (usual: {usual_device})")
    
    # 4. Typing speed anomaly (10 points max)
    typing_speed = transaction_data.get("typing_speed", 0)
    if typing_speed > 150 or typing_speed < 20:
        risk_score += 10
        reasons.append("Unusual typing pattern detected")
    
    # Cap at 100
    risk_score = min(100, risk_score)
    
    # Determine status
    if risk_score < 30:
        status = "APPROVED"
        color = "green"
    elif risk_score < 70:
        status = "REVIEW_NEEDED"
        color = "orange"
    else:
        status = "BLOCKED"
        color = "red"
    
    return {
        "risk_score": risk_score,
        "status": status,
        "color": color,
        "reasons": reasons,
        "timestamp": datetime.now().isoformat()
    }

@app.route('/api/risk-score', methods=['POST'])
def risk_score_endpoint():
    """API endpoint for risk assessment"""
    data = request.json
    user_id = data.get('user_id', 'sarah123')
    
    result = calculate_risk_score(user_id, data)
    return jsonify(result)

@app.route('/api/transactions', methods=['GET'])
def get_transactions():
    """Get recent transactions for dashboard"""
    # Generate mock transaction history
    transactions = []
    for i in range(10):
        amount = random.randint(20, 200)
        risk = random.randint(0, 80) if i < 8 else random.randint(70, 95)
        
        transactions.append({
            "id": i,
            "amount": amount,
            "merchant": ["Amazon", "Starbucks", "Walmart", "Netflix", "Uber"][i % 5],
            "timestamp": f"2024-01-{15+i%10} 14:{30-i%30}:00",
            "risk_score": risk,
            "status": "APPROVED" if risk < 30 else "BLOCKED" if risk > 70 else "REVIEWED"
        })
    
    return jsonify({"transactions": transactions})

@app.route('/api/educational-tip', methods=['GET'])
def get_tip():
    """Get a random educational tip"""
    tips = [
        "Gift cards are the #1 payment method requested by scammers.",
        "Legitimate companies will NEVER ask for payment via wire transfer or gift cards.",
        "Check your credit card statements regularly for unfamiliar charges.",
        "Use strong, unique passwords for each of your financial accounts.",
        "Enable two-factor authentication wherever possible.",
        "If an offer seems too good to be true, it probably is."
    ]
    
    return jsonify({
        "tip": random.choice(tips),
        "category": ["Phishing", "Payment", "Account Security"][random.randint(0, 2)]
    })

@app.route('/')
def serve_frontend():
    """Serve the React frontend"""
    return send_from_directory('../frontend/build', 'index.html')

if __name__ == '__main__':
    app.run(debug=True, port=5000)