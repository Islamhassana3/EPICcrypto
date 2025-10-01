"""
Tests for API endpoints
"""
import pytest
from app import create_app


@pytest.fixture
def client():
    """Create test client"""
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_health_check(client):
    """Test health check endpoint"""
    response = client.get('/api/health')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'healthy'
    assert 'version' in data


def test_get_supported_coins(client):
    """Test supported coins endpoint"""
    response = client.get('/api/coins')
    assert response.status_code == 200
    data = response.get_json()
    assert 'popular' in data
    assert 'all' in data
    assert len(data['popular']) > 0


def test_index_page(client):
    """Test index page loads"""
    response = client.get('/')
    assert response.status_code == 200
    assert b'AI Crypto Prediction' in response.data
