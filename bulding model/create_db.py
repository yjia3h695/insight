# Create database and save weather data
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
import pandas as pd

email, passwd, db_name, db_user, db_pswd = open(
    'login.secret').read().strip().split(',')

# 'engine' is a connection to a database
# Here, we're using postgres, but sqlalchemy can connect to other things too.
engine = create_engine('postgresql://%s:%s@localhost/%s' %
                       (db_user, db_pswd, db_name))
# Replace localhost with IP address if accessing a remote server

if not database_exists(engine.url):
    create_database(engine.url)

colume_names = ['date', 'max_tempf', 'mean_tempf', 'min_tempf',
                'max_dew_pointf', 'mean_dew_pointf', 'min_dew_pointf',
                'max_hum', 'mean_hum', 'min_hum', 'max_sea_level_pressure_in',
                'mean_sea_level_pressure_in', 'min_sea_level_pressure_in',
                'max_visibility_miles', 'mean_visibility_miles',
                'min_visibility_miles', 'max_wind_speed', 'mean_wind_speed',
                'max_gust_speed', 'precipitationIn', 'cloudcover',
                'events', 'wind_dir_degrees', 'city', 'city_code']

weather1 = pd.read_csv('data/bos_temp.csv')
weather1['city'] = 'Boston, MA'
weather1['city_code'] = '1'
weather1.columns = colume_names


weather2 = pd.read_csv('data/chicago_temp.csv')
weather2['city'] = 'Chicago, IL'
weather2['city_code'] = '2'
weather2.columns = colume_names

weather3 = pd.read_csv('data/seattle_temp.csv')
weather3['city'] = 'Seattle, WA'
weather3['city_code'] = '3'
weather3.columns = colume_names

weather4 = pd.read_csv('data/dallas_temp.csv')
weather4['city'] = 'DALLAS, TX'
weather4['city_code'] = '4'
weather4.columns = colume_names

weather = weather1.append(weather2, ignore_index=True).append(
    weather3, ignore_index=True).append(weather4, ignore_index=True)
weather.columns = colume_names
weather.to_csv('data/temp.csv')
weather = pd.read_csv('data/temp.csv')
weather['date'] = pd.to_datetime(weather['date'].astype(str))

weekday = []
for date_n in weather['date']:
    dayofWeek = date_n.dayofweek
    weekday.append(dayofWeek)
weather['dayofweek'] = weekday

# insert data into database from Python
weather.to_sql('weather_data_table', engine, if_exists='replace')
