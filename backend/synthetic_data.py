"""
Synthetic Data Generator for FraudGuard Lite
Creates mock transaction data with clear patterns for fraud detection.
"""

import random
import json
from datetime import datetime, timedelta
import os

# User behavior profiles - each user has distinct shopping patterns
USER_PROFILES = {
    "sarah123": {
        "name": "Sarah Johnson",
        "normal_hours": [9, 21],  # Shops between 9 AM and 9 PM
        "avg_amount": 85.0,
        "amount_range": [20, 200],
        "usual_device": "iPhone",
        "usual_location": "New York, NY",
        "favorite_merchants": ["Amazon", "Starbucks", "Walmart", "Whole Foods", "Netflix"]
    },
    "john_doe": {
        "name": "John Doe",
        "normal_hours": [18, 23],  # Evening shopper (6 PM - 11 PM)
        "avg_amount": 120.0,
        "amount_range": [50, 300],
        "usual_device": "Windows_PC",
        "usual_location": "Chicago, IL",
        "favorite_merchants": ["Steam", "Best Buy", "Uber Eats", "Apple Store", "Spotify"]
    },
    "emma_w": {
        "name": "Emma Wilson",
        "normal_hours": [10, 16],  # Daytime shopper (10 AM - 4 PM)
        "avg_amount": 65.0,
        "amount_range": [15, 150],
        "usual_device": "MacBook",
        "usual_location": "San Francisco, CA",
        "favorite_merchants": ["Etsy", "Trader Joe's", "Target", "Doordash", "Hulu"]
    }
}

# Merchant categories for generating realistic transactions
MERCHANT_CATEGORIES = {
    "Retail": ["Amazon", "Walmart", "Target", "Best Buy", "Apple Store"],
    "Food": ["Starbucks", "McDonald's", "Uber Eats", "Doordash", "Pizza Hut"],
    "Entertainment": ["Netflix", "Spotify", "Steam", "Hulu", "Movie Theater"],
    "Services": ["Uber", "Lyft", "Airbnb", "Gas Station", "Utility Company"],
    "Subscriptions": ["Adobe Creative", "Microsoft 365", "Gym Membership", "News Site"]
}

# Common fraudulent patterns
FRAUD_PATTERNS = [
    {"type": "gift_card_spree", "amount_multiplier": 3.0, "merchants": ["GiftCardMall", "GameStop", "Target"]},
    {"type": "electronics_overseas", "amount_multiplier": 5.0, "merchants": ["Apple Store", "Best Buy", "Newegg"]},
    {"type": "midnight_shopping", "amount_multiplier": 2.5, "merchants": ["Walmart", "Gas Station", "Online Casino"]}
]

def generate_legitimate_transaction(user_id=None, days_ago=0):
    """
    Generate a legitimate-looking transaction based on user's normal behavior.
    """
    if user_id is None:
        user_id = random.choice(list(USER_PROFILES.keys()))
    
    profile = USER_PROFILES[user_id]
    
    # Generate timestamp within user's normal hours
    hour = random.randint(profile["normal_hours"][0], profile["normal_hours"][1] - 1)
    minute = random.randint(0, 59)
    
    # Create timestamp (some days in the past for history)
    transaction_time = datetime.now() - timedelta(days=days_ago)
    transaction_time = transaction_time.replace(hour=hour, minute=minute, second=random.randint(0, 59))
    
    # Generate amount based on user's typical spending
    base_amount = profile["avg_amount"]
    amount_variation = random.uniform(0.7, 1.3)  # +/- 30% variation
    amount = round(base_amount * amount_variation, 2)
    
    # Choose a merchant from user's favorites (80% chance) or random (20% chance)
    if random.random() < 0.8:
        merchant = random.choice(profile["favorite_merchants"])
    else:
        all_merchants = [m for category in MERCHANT_CATEGORIES.values() for m in category]
        merchant = random.choice(all_merchants)
    
    # Generate realistic typing speed (characters per minute)
    typing_speed = random.randint(40, 120)  # Normal human typing speed
    
    # Calculate a low risk score for legitimate transactions
    risk_score = random.randint(5, 25)
    
    return {
        "transaction_id": f"tx_{random.randint(10000, 99999)}",
        "user_id": user_id,
        "user_name": profile["name"],
        "amount": amount,
        "merchant": merchant,
        "category": next((cat for cat, merchants in MERCHANT_CATEGORIES.items() 
                         if merchant in merchants), "Other"),
        "timestamp": transaction_time.isoformat(),
        "device": profile["usual_device"],
        "location": profile["usual_location"],
        "typing_speed": typing_speed,
        "risk_score": risk_score,
        "status": "APPROVED",
        "is_fraudulent": False
    }

def generate_fraudulent_transaction(user_id=None):
    """
    Generate a transaction with clear fraud indicators.
    """
    if user_id is None:
        user_id = random.choice(list(USER_PROFILES.keys()))
    
    profile = USER_PROFILES[user_id]
    fraud_pattern = random.choice(FRAUD_PATTERNS)
    
    # Unusual time (outside normal hours)
    if fraud_pattern["type"] == "midnight_shopping":
        hour = random.choice([0, 1, 2, 3, 4, 5])  # Very early morning
    else:
        hour = random.randint(profile["normal_hours"][1] + 1, 23)  # After normal hours
    
    transaction_time = datetime.now().replace(hour=hour, minute=random.randint(0, 59))
    
    # Unusually large amount
    base_amount = profile["avg_amount"]
    amount = round(base_amount * fraud_pattern["amount_multiplier"] * random.uniform(0.9, 1.1), 2)
    
    # Unusual merchant (not in user's favorites)
    merchant = random.choice(fraud_pattern["merchants"])
    
    # Suspicious typing speed (either too fast or inconsistent)
    typing_speed = random.choice([random.randint(180, 250),  # Too fast
                                  random.randint(10, 30)])   # Too slow
    
    # New/unusual device
    device = random.choice(["Unknown_Device", "Emulator", "Virtual_Machine", "Tor_Browser"])
    
    # High risk score
    risk_score = random.randint(75, 98)
    
    return {
        "transaction_id": f"tx_{random.randint(10000, 99999)}",
        "user_id": user_id,
        "user_name": profile["name"],
        "amount": amount,
        "merchant": merchant,
        "category": "High Risk",
        "timestamp": transaction_time.isoformat(),
        "device": device,
        "location": random.choice(["Overseas", "VPN Detected", "Unknown"]),
        "typing_speed": typing_speed,
        "risk_score": risk_score,
        "status": "BLOCKED",
        "is_fraudulent": True,
        "fraud_pattern": fraud_pattern["type"]
    }

def generate_transaction_history(user_id=None, num_transactions=50, fraud_percentage=0.2):
    """
    Generate a mix of legitimate and fraudulent transactions.
    
    Args:
        user_id: Specific user or random if None
        num_transactions: Total number of transactions to generate
        fraud_percentage: Percentage of transactions that are fraudulent (0.0 to 1.0)
    """
    history = []
    num_fraud = int(num_transactions * fraud_percentage)
    num_legit = num_transactions - num_fraud
    
    # Generate legitimate transactions (spread over past 30 days)
    for i in range(num_legit):
        days_ago = random.randint(1, 30)
        history.append(generate_legitimate_transaction(user_id, days_ago))
    
    # Generate fraudulent transactions (recent)
    for i in range(num_fraud):
        history.append(generate_fraudulent_transaction(user_id))
    
    # Sort by timestamp (most recent first)
    history.sort(key=lambda x: x["timestamp"], reverse=True)
    
    # Add sequence numbers
    for i, tx in enumerate(history):
        tx["sequence"] = i + 1
    
    return history

def save_to_json(transactions, filename="transactions.json"):
    """
    Save generated transactions to a JSON file.
    """
    os.makedirs("../demo_data", exist_ok=True)
    filepath = os.path.join("../demo_data", filename)
    
    with open(filepath, "w") as f:
        json.dump(transactions, f, indent=2, default=str)
    
    print(f"✅ Saved {len(transactions)} transactions to {filepath}")
    return filepath

def generate_demo_dataset():
    """
    Generate a complete demo dataset for all users.
    """
    all_transactions = []
    
    for user_id in USER_PROFILES.keys():
        user_history = generate_transaction_history(
            user_id=user_id,
            num_transactions=30,
            fraud_percentage=0.25  # 25% fraudulent for demo
        )
        all_transactions.extend(user_history)
    
    # Sort all by timestamp
    all_transactions.sort(key=lambda x: x["timestamp"], reverse=True)
    
    # Save to file
    return save_to_json(all_transactions, "demo_transactions.json")

# Example usage when run directly
if __name__ == "__main__":
    print("🔄 Generating synthetic transaction data...")
    
    # Generate for a specific user
    print("\n📊 Sample legitimate transaction:")
    legit_tx = generate_legitimate_transaction("sarah123")
    print(json.dumps(legit_tx, indent=2, default=str))
    
    print("\n🚨 Sample fraudulent transaction:")
    fraud_tx = generate_fraudulent_transaction("sarah123")
    print(json.dumps(fraud_tx, indent=2, default=str))
    
    print("\n📈 Generating full demo dataset...")
    filepath = generate_demo_dataset()
    print(f"Demo data ready! File saved to: {filepath}")
    
    print("\n🎯 Use this data in your app by calling:")
    print("from synthetic_data import generate_transaction_history")
    print("transactions = generate_transaction_history(num_transactions=100)")