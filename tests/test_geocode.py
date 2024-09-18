from decimal import Decimal
import pytest

from src.services.geocode import create_geocode_url, get_location_data


def test_url():
    assert 'api.mapbox' in create_geocode_url(1, 2)
    assert 'latitude=44.0' in create_geocode_url(44, 55)
    assert 'api.mapbox' in create_geocode_url(Decimal(44), Decimal(55))
    with pytest.raises(ValueError, match='Not a decimal value'):
        create_geocode_url('a', 'b')


def test_location_data(coords):
    for i in coords:
        url = create_geocode_url(i.lat, i.long)
        if i.name == 'Черное море':
            with pytest.raises(ValueError, match='Неверные координаты'):
                get_location_data(url)
        else:
            assert i.name in get_location_data(url)['region']


def test_crimea():
    url = create_geocode_url(44.606757, 33.494303)
    region = get_location_data(url)
    assert region['region'] == 'Севастополь'
    assert region['country'] == 'Россия'
    url = create_geocode_url(45.593884, 34.433780)
    region = get_location_data(url)
    assert region['region'] == 'Республика Крым'
    assert region['country'] == 'Россия'
