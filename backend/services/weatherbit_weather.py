import random

import requests
import json
from enum import Enum
from pydantic import BaseModel
from typing import NamedTuple


class Coords(NamedTuple):
    altitude: float
    longitude: float


class WeatherCode(Enum):
    THUNDERSTORM_LIGHT_RAIN: int = 200
    THUNDERSTORM_MEDIUM_RAIN: int = 201
    THUNDERSTORM_HEAVY_RAIN: int = 202
    THUNDERSTORM_LIGHT_DRIZZLE: int = 230
    THUNDERSTORM_MEDIUM_DRIZZLE: int = 231
    THUNDERSTORM_HEAVY_DRIZZLE: int = 232
    THUNDERSTORM_HAIL: int = 233
    DRIZZLE_LIGHT: int = 300
    DRIZZLE_MEDIUM: int = 301
    DRIZZLE_HEAVY: int = 302
    RAIN_LIGHT: int = 500
    RAIN_MEDIUM: int = 501
    RAIN_HEAVY: int = 502
    RAIN_FREEZING: int = 511
    RAIN_SHOWER_LIGHT: int = 520
    RAIN_SHOWER_MEDIUM: int = 521
    RAIN_SHOWER_HEAVY: int = 522
    SNOW_LIGHT: int = 600
    SNOW_MEDIUM: int = 601
    SNOW_HEAVY: int = 602
    SNOW_MIX: int = 601
    SLEET_MEDIUM: int = 611
    SLEET_HEAVY: int = 612
    SNOW_SHOWER: int = 621
    SNOW_SHOWER_HEAVY: int = 622
    FLURRIES: int = 623
    MIST: int = 700
    SMOKE: int = 711
    HAZE: int = 721
    SAND_DUST: int = 731
    FOG: int = 741
    FREEZING_FOG: int = 751
    CLEAR_SKY: int = 800
    CLOUDS_FEW: int = 801
    CLOUDS_SCATTERED: int = 802
    CLOUDS_BROKEN: int = 803
    CLOUDS_OVERCAST: int = 804
    UNKNOWN: int = 900


class WeatherDescription(BaseModel):
    description: str
    code: WeatherCode


class ResponseData(BaseModel):
    weather: WeatherDescription


class Weather(BaseModel):
    data: list[ResponseData]


def get_weather_by_coords(coords: Coords) -> Weather:
    """ Получение погоды по координатам"""

    # Обращение к API
    data = _get_random_response(coords)

    return data


def _get_random_response(_) -> Weather:
    return Weather(**{'data': [{'weather': {'description': "fog", 'code': random.choice(list(WeatherCode))}}]})


def _get_api_response(coords) -> Weather:
    """ Обращается к API OpenWeather"""
    """curl -X GET --header 'Accept: application/json' 'https://api.weatherbit.io/v2.0/current?lat=43&lon=130&key=3bf4d35c3c0c47709f8495c92920924d'"""
    alt, lon = coords
    response = requests.get(
        'https://api.weatherbit.io/v2.0/current',
        headers={
            "Accept": "application/json",
        },
        params={
            'lat': alt,
            'lon': lon,
            'key': '3bf4d35c3c0c47709f8495c92920924d'
        }
    )
    if json.loads(response.content.decode('utf-8')).get('status_code'):
        return Weather(**{'data': [{'weather': {'description': "fog", 'code': random.choice(list(WeatherCode))}}]})

    return Weather(**json.loads(response.content.decode('utf-8')))


if __name__ == "__main__":
    print(get_weather_by_coords(Coords(altitude=50, longitude=100)))
