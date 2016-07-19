from read_db import read_db
from sklearn.cross_validation import train_test_split

weather, running, full, stat = read_db()

datasets = stat[['count', 'dayofweek', 'mean_tempf', 'max_tempf',
                 'precipitationIn', 'mean_dew_pointf', 'mean_hum',
                 'mean_wind_speed', 'wind_dir_degrees',
                 'mean_visibility_miles', 'cloudcover',
                 'mean_sea_level_pressure_in', 'events']]

datasets['events'] = datasets['events'].fillna(value='Clear')
datasets['id'] = datasets['events'].astype('category').cat.codes
datasets['precipitationIn'] = datasets['precipitationIn'].replace('T', 0)
datasets['precipitationIn'] = datasets['precipitationIn'].astype(float)
datasets = datasets.dropna().drop('events', 1)
datasets = datasets.astype(int)

X = datasets[['dayofweek', 'mean_tempf', 'max_tempf', 'precipitationIn',
              'mean_dew_pointf', 'mean_hum', 'mean_wind_speed', 'wind_dir_degrees',
              'mean_visibility_miles', 'cloudcover', 'mean_sea_level_pressure_in']]

y = datasets['count']

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42)
#X_train,X_vali,y_train,y_vali=train_test_split(X_train,y_train,test_size = 0.25,random_state=42)
