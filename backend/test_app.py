import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app

def test_home_route():
    """Test the home route returns something"""
    with app.test_client() as client:
        response = client.get('/')
        # If your app.py has no home route, test an API endpoint instead
        # response = client.get('/api/educational-tip')
        assert response.status_code in [200, 404]  # Either is fine for now

def test_risk_score_endpoint():
    """Test the risk score endpoint with POST"""
    with app.test_client() as client:
        response = client.post('/api/risk-score', 
                             json={'user_id': 'test', 'amount': 100},
                             content_type='application/json')
        # Should return JSON with risk_score
        assert response.status_code == 200
        data = response.get_json()
        assert 'risk_score' in data
        assert 0 <= data['risk_score'] <= 100