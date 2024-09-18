def test_map(client):
    resp = client.get('/map')
    assert resp.status_code == 302
