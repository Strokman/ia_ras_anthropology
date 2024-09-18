import pytest
from collections import namedtuple
import base_habilis


@pytest.fixture()
def app():
    app = base_habilis.create_app()
    app.config.update({
        "TESTING": True,
    })
    yield app


@pytest.fixture()
def client(app):
    yield app.test_client()


@pytest.fixture()
def coords():
    Region = namedtuple('Region', ['name', 'lat', 'long'])
    region1 = Region('Липецкая', 52.272448, 39.936757)
    region2 = Region('Новосибирская', 54.951675, 83.419989)
    region3 = Region('Абхазия', 43.030841, 41.024124)
    region4 = Region('Черное море', 42.952468, 35.858094)
    region5 = Region('Севастополь', 44.606757, 33.494303)
    region6 = Region('Республика Крым', 45.593884, 34.433780)
    regions = (region1, region2, region3, region4, region5, region6)
    return regions
