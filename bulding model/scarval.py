#!/usr/bin/python
# -*- coding: utf-8 -*-
import stravalib
import BaseHTTPServer
import urlparse
import webbrowser
import pandas as pd
import datetime

# Global Variables - put your data in the file 'client.secret' and
# separate the fields with a comma!
client_id, secret = open('client.secret').read().strip().split(',')
port = 5000
url = 'http://localhost:%d/authorized' % port
allDone = False
types = ['time', 'distance', 'latlng', 'altitude',
         'velocity_smooth', 'moving', 'grade_smooth', 'temp']
limit = 15

# Create the strava client, and open the web browser for authentication
client = stravalib.client.Client()
authorize_url = client.authorization_url(client_id=client_id, redirect_uri=url)
print 'Opening: %s' % authorize_url
webbrowser.open(authorize_url)

# Define the web functions to call from the strava API


def UseCode(code):
    # Retrieve the login code from the Strava server
    access_token = client.exchange_code_for_token(client_id=client_id,
                                                  client_secret=secret, code=code)
    # Now store that access token somewhere (for now, it's just a local
    # variable)
    client.access_token = access_token
    athlete = client.get_athlete()
    print("For %(id)s, I now have an access token %(token)s" %
          {'id': athlete.id, 'token': access_token})
    return client


def getSegmentEfforts(client, limit):
    # Returns a list of Strava activity objects, up to the number specified by
    # limit
    segment_efforts = client.get_segment_efforts(5694228, limit=limit)
    assert len(list(segment_efforts)) == limit
    for item in segment_efforts:
        print item
    return segment_efforts


def ParseActivity(act, types):
    act_id = act.id
    name = act.name
    print str(act_id), str(act.name), act.start_date
    streams = GetStreams(client, act_id, types)
    df = pd.DataFrame()

    # Write each row to a dataframe
    for item in types:
        if item in streams.keys():
            df[item] = pd.Series(streams[item].data, index=None)
        df['act_id'] = act.id
        df['act_startDate'] = pd.to_datetime(act.start_date)
        df['act_name'] = name
    return df


def GetStreams(client, activity, types):
    # Returns a Strava 'stream', which is timeseries data from an activity
    streams = client.get_activity_streams(
        activity, types=types, series_type='time')
    return streams


def DataFrame(dict, types):
    # Converts a Stream into a dataframe, and returns the dataframe
    print dict, types
    df = pd.DataFrame()
    for item in types:
        if item in dict.keys():
            df.append(item.data)
    df.fillna('', inplace=True)
    return df


def calctime(time_sec, startdate):
    try:
        timestamp = startdate + datetime.timedelta(seconds=int(time_sec))
    except:
        print 'time processing error : ' + str(time_sec)
        timestamp = startdate
    return timestamp


def split_lat(series):
    lat = series[0]
    return lat


def split_long(series):
    long = series[1]
    return long


def concatdf(df_lst):
    return pd.concat(df_lst, ignore_index=False)


class MyHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    # Handle the web data sent from the strava API

    def do_HEAD(self):
        return self.do_GET()

    def do_GET(self):
        # Get the API code for Strava
        self.wfile.write('<script>window.close();</script>')
        code = urlparse.parse_qs(urlparse.urlparse(self.path).query)['code'][0]

        # Login to the API
        client = UseCode(code)

        # Retrieve the last limit activities
        segmentEfforts = getSegmentEfforts(client, limit)

        # Loop through the activities, and create a dict of the dataframe
        # stream data of each activity
        print "looping through activities..."
        df_lst = {}
        for users in segmentEfforts:
            df_lst[users.start_date] = ParseActivity(users, types)

###Run the program to login and grab data###
httpd = BaseHTTPServer.HTTPServer(('localhost', port), MyHandler)
while not allDone:
    httpd.handle_request()
