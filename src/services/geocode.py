import requests
import config
from decimal import Decimal


def create_geocode_url(lat, long):
    try:
        lat, long = float(lat), float(long)
        url = f'https://api.mapbox.com/search/geocode/v6/reverse?longitude={long}&latitude={lat}&access_token={config.Config.MAPBOX_TOKEN}&language=ru'
        return url
    except ValueError:
        raise ValueError('Not a decimal value')
    # if not isinstance(long, (Decimal, float)) and not isinstance(lat, (Decimal, float)):
    #     raise ValueError('Not a decimal value')
    
    # return url


def get_location_data(url):
    try:
        resp = requests.get(url).json()['features'][0]['properties']['context']
        region_data = {}
        region_data['country'] = resp['country']['name']
                # case 'region':
        region_data['region'] = resp['region']['name']
        if region_data['region'] in ('Автономная Республика Крым', 'Севастополь'):
            region_data['country'] = 'Россия'
                # case 'area' if 'region' not in region_data:
                #     region_data['region'] = i['name']
                # case 'locality' if 'region' not in region_data:
                #     region_data['region'] = i['name']
        if region_data['region'] == 'Автономная Республика Крым':
            region_data['region'] = 'Республика Крым'
        return region_data
    except IndexError:
        raise ValueError('Неверные координаты')
