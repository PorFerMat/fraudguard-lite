"""
Mock Machine Learning Model for FraudGuard Lite
A lightweight fraud detector using rule-based thresholds that mimics ML behavior.
"""

import json
import random
from datetime import datetime

class FraudDetector:
    """
    A simplified fraud detection model that learns patterns from historical data
    and makes predictions based on learned thresholds.
    """
    
    def __init__(self):
        self.user_profiles = {}
        self.global_thresholds = {
            'amount_anomaly': 2.5,      # Transactions > 2.5x average are suspicious
            'time_anomaly': 4,          # Hours outside normal range
            'typing_anomaly_low': 30,   # Too slow typing (characters/minute)
            'typing_anomaly_high': 150, # Too fast typing
            'device_risk_score': 0.7    # New device risk weight
        }
        self.model_confidence = 0.92    # Mock model confidence score
        self.is_trained = False
    
    def train(self, historical_data):
        """
        'Train' the model by analyzing historical transaction patterns.
        In a real system, this would use ML algorithms.
        """
        print("🤖 Training fraud detection model...")
        
        # Analyze each user's normal behavior
        for transaction in historical_data:
            user_id = transaction.get('user_id')
            if user_id not in self.user_profiles:
                self.user_profiles[user_id] = {
                    'transaction_count': 0,
                    'amounts': [],
                    'devices': set(),
                    'hours': [],
                    'merchants': set()
                }
            
            profile = self.user_profiles[user_id]
            profile['transaction_count'] += 1
            profile['amounts'].append(transaction['amount'])
            profile['devices'].add(transaction.get('device', 'unknown'))
            
            # Extract hour from timestamp
            try:
                hour = datetime.fromisoformat(transaction['timestamp'].replace('Z', '')).hour
                profile['hours'].append(hour)
            except:
                pass
            
            profile['merchants'].add(transaction['merchant'])
        
        # Calculate statistics for each user
        for user_id, profile in self.user_profiles.items():
            if profile['amounts']:
                profile['avg_amount'] = sum(profile['amounts']) / len(profile['amounts'])
                profile['max_amount'] = max(profile['amounts'])
                profile['min_amount'] = min(profile['amounts'])
            
            if profile['hours']:
                # Find most common shopping hours (simplified)
                hour_counts = {}
                for hour in profile['hours']:
                    hour_counts[hour] = hour_counts.get(hour, 0) + 1
                common_hours = sorted(hour_counts.items(), key=lambda x: x[1], reverse=True)[:4]
                profile['common_hours'] = [h[0] for h in common_hours]
        
        self.is_trained = True
        print(f"✅ Model trained on {len(historical_data)} transactions for {len(self.user_profiles)} users")
        return self
    
    def predict(self, transaction_data, user_id='sarah123'):
        """
        Predict fraud probability for a transaction.
        Returns: risk_score (0-100), reasons, confidence
        """
        if not self.is_trained:
            # Fallback to simple rules if not trained
            return self._fallback_prediction(transaction_data, user_id)
        
        risk_score = 0
        reasons = []
        
        # Get user profile or create default
        profile = self.user_profiles.get(user_id, {
            'avg_amount': 100,
            'common_hours': [9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20],
            'devices': {'iPhone', 'Windows_PC'}
        })
        
        # 1. Amount anomaly check
        amount = transaction_data.get('amount', 0)
        avg_amount = profile.get('avg_amount', 100)
        
        if amount > avg_amount * self.global_thresholds['amount_anomaly']:
            amount_risk = min(40, (amount / avg_amount) * 15)
            risk_score += amount_risk
            reasons.append(f"Amount (${amount}) is {amount/avg_amount:.1f}x higher than average (${avg_amount})")
        
        # 2. Time anomaly check
        try:
            hour = datetime.fromisoformat(transaction_data.get('timestamp', '').replace('Z', '')).hour
            common_hours = profile.get('common_hours', [9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20])
            
            if hour not in common_hours:
                # Calculate how unusual this hour is
                closest_hour = min(common_hours, key=lambda x: abs(x - hour))
                hour_diff = abs(hour - closest_hour)
                time_risk = min(30, hour_diff * 3)
                risk_score += time_risk
                reasons.append(f"Transaction at {hour}:00 is outside normal shopping hours ({min(common_hours)}:00-{max(common_hours)}:00)")
        except:
            pass
        
        # 3. Device anomaly check
        device = transaction_data.get('device', 'unknown')
        known_devices = profile.get('devices', {'iPhone', 'Windows_PC'})
        
        if device not in known_devices:
            risk_score += 20
            reasons.append(f"New/unusual device detected: {device}")
        
        # 4. Typing speed anomaly
        typing_speed = transaction_data.get('typing_speed', 0)
        if typing_speed < self.global_thresholds['typing_anomaly_low']:
            risk_score += 15
            reasons.append(f"Unusually slow typing speed: {typing_speed} chars/min")
        elif typing_speed > self.global_thresholds['typing_anomaly_high']:
            risk_score += 15
            reasons.append(f"Unusually fast typing speed: {typing_speed} chars/min")
        
        # Cap at 100 and determine status
        risk_score = min(100, risk_score)
        
        # Add some random variation to simulate ML uncertainty
        if 30 < risk_score < 70:
            risk_score += random.randint(-10, 10)
            risk_score = max(0, min(100, risk_score))
        
        # Determine status
        if risk_score < 25:
            status = "APPROVED"
            color = "green"
        elif risk_score < 65:
            status = "REVIEW_NEEDED"
            color = "orange"
        else:
            status = "BLOCKED"
            color = "red"
        
        return {
            "risk_score": round(risk_score, 1),
            "status": status,
            "color": color,
            "reasons": reasons,
            "model_confidence": self.model_confidence,
            "model_version": "1.0.0"
        }
    
    def _fallback_prediction(self, transaction_data, user_id):
        """Fallback prediction if model isn't trained"""
        risk_score = 0
        reasons = []
        
        # Simple rule-based fallback
        amount = transaction_data.get('amount', 0)
        if amount > 300:
            risk_score += 40
            reasons.append(f"High transaction amount: ${amount}")
        
        device = transaction_data.get('device', '')
        if 'unknown' in device.lower() or 'emulator' in device.lower():
            risk_score += 30
            reasons.append(f"Suspicious device: {device}")
        
        typing_speed = transaction_data.get('typing_speed', 0)
        if typing_speed > 200 or typing_speed < 20:
            risk_score += 20
            reasons.append(f"Abnormal typing speed: {typing_speed}")
        
        risk_score = min(100, risk_score)
        
        return {
            "risk_score": risk_score,
            "status": "BLOCKED" if risk_score > 60 else "APPROVED",
            "color": "red" if risk_score > 60 else "green",
            "reasons": reasons,
            "model_confidence": 0.75,
            "model_version": "0.5.0 (fallback)"
        }
    
    def get_model_info(self):
        """Get information about the trained model"""
        return {
            "is_trained": self.is_trained,
            "users_trained": len(self.user_profiles),
            "confidence": self.model_confidence,
            "version": "1.0.0",
            "thresholds": self.global_thresholds
        }

# Helper function to generate mock model explanations (for dashboard)
def generate_feature_importance():
    """Generate mock feature importance for visualization"""
    return {
        "transaction_amount": 0.35,
        "transaction_time": 0.25,
        "user_device": 0.20,
        "typing_pattern": 0.15,
        "merchant_category": 0.05
    }

def generate_training_metrics():
    """Generate mock training metrics"""
    return {
        "accuracy": 0.94,
        "precision": 0.91,
        "recall": 0.89,
        "f1_score": 0.90,
        "training_samples": 1250,
        "false_positive_rate": 0.05
    }

# Singleton instance for easy access
fraud_detector = FraudDetector()