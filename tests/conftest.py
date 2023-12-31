import pytest
import base_habilis
# from ia_ras_anthropology.anthropos import create_app

@pytest.fixture()
def app():
    app = base_habilis.create_app()
    app.config.update({
        "TESTING": True,
    })

    yield app


@pytest.fixture()
def client(app):
    return app.test_client()


def test_map(client):
    resp = client.get('/map')

    assert resp.status_code == 200