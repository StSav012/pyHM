# coding=utf-8
from json import loads
from contextlib import suppress
from typing import Iterable, TypedDict, cast
from urllib.request import urlopen
from datetime import datetime, timedelta, timezone, tzinfo

__all__ = [
    "guess_weather",
    "guess_position",
    "LATITUDE",
    "LONGITUDE",
    "ELEVATION",
    "CLOUD_COVER",
    "PRECIPITATION",
    "WEATHER_CODE",
    "WEATHER_CODE_MEANINGS",
]


class GeoDataType(TypedDict, total=False):
    country_code: str
    country_name: str
    city: str
    postal: str
    latitude: float
    longitude: float
    IPv4: str
    state: str


def guess_position() -> tuple[float, float]:
    with suppress(Exception), urlopen(
        url="https://geolocation-db.com/json",
        timeout=1,
    ) as url:
        data: GeoDataType = loads(url.read())
        return data["latitude"], data["longitude"]

    tz_info: tzinfo | None = datetime.now(timezone.utc).astimezone().tzinfo
    if tz_info is not None:
        tz_offset: timedelta | None = tz_info.utcoffset(None)
        if tz_offset is not None:
            return 0.0, tz_offset.total_seconds() / 240.0

    return 0.0, 0.0


class CurrentUnitsType(TypedDict, total=False):
    time: str
    interval: str
    weather_code: str


class CurrentDataType(TypedDict, total=False):
    time: str
    interval: int
    weather_code: int
    cloud_cover: int
    precipitation: int


class WeatherDataType(TypedDict, total=False):
    latitude: float
    longitude: float
    generationtime_ms: float
    utc_offset_seconds: int
    timezone: str
    timezone_abbreviation: str
    elevation: int

    current_units: CurrentUnitsType
    current: CurrentDataType


def guess_weather(
    latitude: float, longitude: float, current_conditions: Iterable[str]
) -> WeatherDataType:
    params: dict[str, float | Iterable[str]] = {
        "latitude": latitude,
        "longitude": longitude,
        "current": current_conditions,
    }
    encoded_params: str = "&".join(
        (
            f"{key}={value}"
            if not isinstance(value, Iterable) or isinstance(value, str)
            else key + "=" + ",".join(value)
        )
        for key, value in params.items()
    )
    with suppress(Exception), urlopen(
        url=f"https://api.open-meteo.com/v1/forecast?{encoded_params}",
        timeout=1,
    ) as url:
        data: WeatherDataType = loads(url.read())
        return data
    return {}


LATITUDE, LONGITUDE = guess_position()
_weather: WeatherDataType = guess_weather(
    LATITUDE,
    LONGITUDE,
    ("weather_code", "cloud_cover", "precipitation"),
)
ELEVATION: int = _weather.get("elevation", 0)
CLOUD_COVER: int = cast(CurrentDataType, _weather.get("current", {})).get(
    "cloud_cover", -1
)
PRECIPITATION: float = cast(CurrentDataType, _weather.get("current", {})).get(
    "precipitation", -1
)
WEATHER_CODE: int = cast(CurrentDataType, _weather.get("current", {})).get(
    "weather_code", -1
)
WEATHER_CODE_MEANINGS: dict[int, str] = {
    0: "clear",
    1: "mainly clear",
    2: "partly cloudy",
    3: "overcast",
    45: "fog",
    48: "depositing rime fog",
    51: "light drizzle",
    53: "moderate drizzle",
    55: "intense drizzle",
    61: "light rain",
    63: "moderate rain",
    65: "intense rain",
    66: "light freezing rain",
    67: "intense freezing rain",
    71: "light snow fall",
    73: "moderate snow fall",
    75: "intense snow fall",
    77: "snow grains",
    80: "slight rain shower",
    81: "moderate rain shower",
    82: "violent rain shower",
    85: "slight rain shower",
    86: "heavy rain shower",
    95: "thunderstorm",
    96: "thunderstorm with slight hail",
    99: "thunderstorm with heavy hail",
}
