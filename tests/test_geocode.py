from src.services.geocode import create_geocode_url, get_location_data
from tests.conftest import client
from decimal import Decimal

import pytest


def test_url():
    assert 'api.mapbox' in create_geocode_url(1, 2)
    assert 'latitude=44.0' in create_geocode_url(44, 55)
    assert 'api.mapbox' in create_geocode_url(Decimal(44), Decimal(55))
    with pytest.raises(ValueError, match='Not a decimal value'):
        create_geocode_url('a', 'b')

def test_location_data():
    pass
