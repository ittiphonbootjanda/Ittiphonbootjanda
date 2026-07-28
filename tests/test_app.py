from app import app
def test_app():
    client = app.test_client()
    rv = client.get('/')
    assert rv.status_code == 200
    assert b'id="video-form"' in rv.data
    assert b'required' in rv.data
    assert b'visually-hidden' in rv.data
