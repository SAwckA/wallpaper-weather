import json
import requests

from pydantic import BaseModel

from typing import NamedTuple

from enum import Enum


class Coords(NamedTuple):
    altitude: float
    longitude: float


class Location(BaseModel):
    name: str
    region: str
    country: str
    localtime_epoch: int


class Condition(BaseModel):
    text: str
    icon: str
    code: int


class Current(BaseModel):
    last_updated_epoch: int
    temp_c: float
    feelslike_c: float
    condition: Condition
    is_day: int


class Weather(BaseModel):
    location: Location
    current: Current


def get_weather_by_coords(coords: Coords) -> Weather:
    """ Получает данные из api """
    alt, lon = coords
    return _get_weather_from_api(alt, lon)


def _get_weather_from_api(alt, lon) -> Weather:

    response = requests.get('http://api.weatherapi.com/v1/current.json',
                            params={
                                     'key': '1e464f0bb8e8442185a35212222805',
                                     'q': f'{alt}, {lon}',
                                     'aqi': 'no',
                                     'lang': 'ru'
                                    })

    return Weather(**json.loads(response.content.decode('utf-8')))


if __name__ == '__main__':
    print(get_weather_by_coords(Coords(altitude=47, longitude=130)))
