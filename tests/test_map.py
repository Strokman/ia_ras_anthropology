from tests.conftest import client

app = client

def test_map(app):
    resp = app.get('/map')

    assert resp.status_code == 200
