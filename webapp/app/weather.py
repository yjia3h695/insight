import urllib2
import json
from get_location import from_address
import pandas as pd
import math
import datetime

find_now = datetime.datetime.now()
now_reset = find_now.replace(hour=2, minute=0, second=0, microsecond=1)
now = now_reset.isoformat() + 'Z'  # 'Z' indicates UTC time
tomorrow = (now_reset + datetime.timedelta(days=1)).isoformat() + 'Z'
a = pd.to_datetime(tomorrow)
weekday = a.dayofweek


def get_forcast(address):
    lat, lng = from_address(address)
    url = 'https://api.forecast.io/forecast/2191dd33d9cb218e2aff15ac1eba5f41/%f,%f' % (
        lat, lng)
    f = urllib2.urlopen(url)
    json_string = f.read()
    parsed_json = json.loads(json_string)
    precipIntensity = parsed_json['daily']['data'][0]["precipIntensity"]
    # moonPhase = parsed_json['daily']['data'][0]["moonPhase"]
    precipIntensityMax = parsed_json['daily']['data'][0]["precipIntensityMax"]
    # precipProbability = parsed_json['daily']['data'][0]["precipProbability"]
    temperatureMin = parsed_json['daily']['data'][0]["temperatureMin"]
    temperatureMax = parsed_json['daily']['data'][0]["temperatureMax"]
    # apparentTemperatureMax = parsed_json['daily'][
    # 'data'][0]["apparentTemperatureMax"]
    dewPoint = parsed_json['daily']['data'][0]["dewPoint"]
    humidity = parsed_json['daily']['data'][0]["humidity"]
    windSpeed = parsed_json['daily']['data'][0]["windSpeed"]
    windBearing = parsed_json['daily']['data'][0]["windBearing"]
    visibility = parsed_json['daily']['data'][0]["visibility"]
    cloudCover = parsed_json['daily']['data'][0]["cloudCover"]
    pressure = parsed_json['daily']['data'][0]["pressure"]
    # ozone = parsed_json['daily']['data'][0]["ozone"]
    # icon = parsed_json['daily']['data'][0]["icon"]

    df = pd.Series([int(precipIntensity)])
    df['precipitationIn'] = float(precipIntensityMax)
    df['mean_tempf'] = math.ceil(
        (float(temperatureMin) + float(temperatureMax)) / 2.0)
    df['max_tempf'] = float(temperatureMax)
    df['mean_dew_pointf'] = float(dewPoint)
    df['mean_hum'] = float(humidity)
    df['mean_wind_speed'] = float(windSpeed)
    df['wind_dir_degrees'] = float(windBearing)
    df['mean_visibility_miles'] = float(visibility)
    df['cloudcover'] = float(cloudCover)
    df['mean_sea_level_pressure_in'] = (float(pressure) / 33.86)
    df['dayofweek'] = weekday

    df = df[1:]

    f.close()
    return df
