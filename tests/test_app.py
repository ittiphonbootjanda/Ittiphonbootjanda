import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_index_page(client):
    """Test that the index page loads correctly."""
    response = client.get('/')
    assert response.status_code == 200
    assert b'Text to Video Generator' in response.data
    assert b'id="t"' in response.data
    assert b'id="s"' in response.data
    assert b'visually-hidden' in response.data
