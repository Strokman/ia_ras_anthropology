import requests
import config
from decimal import Decimal


def create_geocode_url(lat, long):
    if not isinstance(long, (Decimal, float)) and not isinstance(lat, (Decimal, float)):
        raise ValueError('Not a decimal value')
    url = f'https://geocode-maps.yandex.ru/1.x?apikey={config.Config.YMAPS_API_KEY}&geocode={long}, {lat}&lang=ru_RU&format=json'
    return url


def get_location_data(url):
    resp = requests.get(url).json()['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['metaDataProperty']['GeocoderMetaData']['Address']['Components']
    region_data = {}
    for i in resp:
        match i['kind']:
            case 'country':
                region_data['country'] = i['name']
            case 'province':
                region_data['region'] = i['name']
            case 'area' if 'region' not in region_data:
                region_data['region'] = i['name']
            case 'locality' if 'region' not in region_data:
                region_data['region'] = i['name']
    if not region_data:
        raise ValueError('Неверные координаты')
    return region_data
