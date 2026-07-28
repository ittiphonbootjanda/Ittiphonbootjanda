import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_index_page(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'Text to Video Generator' in response.data
    assert b'Video Text Content' in response.data # Check for the label I added
    assert b'id="text-input"' in response.data
    assert b'id="submit-btn"' in response.data
