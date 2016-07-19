from sqlalchemy import create_engine
import psycopg2
import pandas as pd

email, passwd, db_name, db_user, db_pswd = open(
    'login.secret').read().strip().split(',')
engine = create_engine('postgresql://%s:%s@localhost/%s' %
                       (db_user, db_pswd, db_name))


def read_db():
    con = None
    con = psycopg2.connect(database=db_name, user=db_user,
                           host='localhost', password=db_pswd)

    # query:
    weather_query = """
                    SELECT * FROM weather_data_table;
                    """

    record_query = """
                   SELECT * FROM running_data_table;
                   """

    stat_query = """
                 SELECT date, city, COUNT(city)
                 FROM running_data_table
                 GROUP BY date,city;
                 """
    # read database
    weather_data = pd.read_sql_query(weather_query, con)

    running_data = pd.read_sql_query(record_query, con)

    stat_data = pd.read_sql_query(stat_query, con)

    stat = pd.merge(weather_data, stat_data, on=['date', 'city'])

    full = pd.merge(weather_data, running_data, on=['date', 'city'])
    full.to_sql('full_data_table', engine, if_exists='replace')

    return weather_data, running_data, full, stat
