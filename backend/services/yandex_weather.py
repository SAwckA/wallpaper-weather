""" Модуль для работы с погодой, реализован только апи OpenWeather"""
import json
from enum import Enum

import requests

from pydantic import BaseModel
from typing import NamedTuple


class APIError(Exception):
    pass


class Coords(NamedTuple):
    altitude: float
    longitude: float


class InfoPlace(BaseModel):
    lat: float
    lon: float
    url: str


class Condition(Enum):
    CLEAR = 'clear'


class WindDirection(Enum):
    NW = 'nw'
    N = 'n'
    NE = 'ne'
    E = 'e'
    SE = 'se'
    S = 's'
    SW = 'sw'
    W = 'w'
    C = 'c'


class Daytime(Enum):
    D = 'd'
    N = 'n'


class Season(Enum):
    SUMMER = 'summer'
    AUTUMN = 'autumn'
    WINTER = 'winter'
    SPRING = 'spring'


class FactWeather(BaseModel):
    temp: int
    feels_like: int
    temp_water: int = None
    icon: str
    condition: str
    wind_speed: int
    wind_gust: int
    wind_dir: WindDirection
    pressure_mm: int
    pressure_pa: int
    humidity: int
    daytime: Daytime
    polar: bool
    season: Season
    obs_time: int


class Weather(BaseModel):
    """ Pydantic класс представления погоды """
    now: int
    now_dt: str
    info: InfoPlace
    fact: FactWeather


def get_weather_by_coords(coords: Coords) -> Weather:
    """ Получение погоды по координатам"""

    # Обращение к API
    data = _get_api_response(coords)

    return data


def _get_api_response(coords) -> Weather:
    """ Обращается к API OpenWeather"""
    response = requests.get('https://api.weather.yandex.ru/v2/informers', params={
        'lat': coords.altitude,
        'lon': coords.longitude,
        'lan': '[ru_RU]'
    },# a1366f84-2e5e-444a-9e53-e985f7dc14fc
                            #0a426533-1235-4827-969e-396edac31787
                 headers={'X-Yandex-API-Key': '0a426533-1235-4827-969e-396edac31787'})

    if 'Forbidden' in response.content.decode('utf-8'):
        raise APIError

    return Weather(**json.loads(response.content.decode('utf-8')))


if __name__ == "__main__":
    r = _get_api_response(Coords(altitude=53.10, longitude=56.10))

    print(r)
