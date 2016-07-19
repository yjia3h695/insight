#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import print_function
import httplib2
import os
import pandas as pd

from apiclient import discovery
import oauth2client
from oauth2client import client
from oauth2client import tools

from pyrfc3339 import generate, parse
import datetime
from pytz import timezone
import pytz

utc = pytz.utc
eastern = timezone('US/Eastern')

try:
    import argparse
    flags = \
        argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/calendar-python-quickstart.json

SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Google Calendar API Python Quickstart'


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """

    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir,'.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir, 'calendar-python-quickstart.json')

    store = oauth2client.file.Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else:
            print('Storing credentials to ' + credential_path)
    return credentials

def main():
    """
    Creates a Google Calendar API service object and outputs 
    all the events that will happen tomorrow.
    """

    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http = http)

    find_now = datetime.datetime.today()
    zone_dif = datetime.datetime.utcnow()-find_now
    now_reset= find_now.replace(hour = 23, minute =59, second =0, microsecond =0)+zone_dif
    now = now_reset.isoformat()+"Z"  # 'Z' indicates UTC time
    tomorrow = (now_reset + datetime.timedelta(days = 1)).isoformat() +"Z"
    
    desireLocation = \
                raw_input('''
                            Please input your prefered address
                            (Default: 50 milk st, Boston, MA, 02109, enter to change):
                          ''') \
                  or '50 Milk St, Boston, MA, 02109'

    calIDlistResults = service.calendarList().list().execute()
    calIDlists = calIDlistResults.get('items', [])

    print('Today is ', datetime.datetime.today().date())
    print('Searching for your  schedule tomorrow...')
    print('Your avaible schedule between 7:00 am to 9:00 pm is:\n')

    getToday = datetime.datetime.today() + datetime.timedelta(days=1)
    dayStart = getToday.replace(hour=7,  minute=0, second=0, microsecond=0)
    dayEnd   = getToday.replace(hour=21, minute=0, second=0, microsecond=0)

    A = []
    B = []
    C = []
    D = []
    E = []
    F = []

    for calIDlist in calIDlists:
        # for calIDlist in calIDlists[0]:

        # Get calendar ID and get events in this calendar
        calID = calIDlist.get('id')
        eventsResult = service.events().list(calendarId=calID, timeMin=now,
                                             timeMax=tomorrow).execute()
        events = eventsResult.get('items', [])

        for event in events:
            start = parse(event['start'].get('dateTime'))
            end = parse(event['end'].get('dateTime'))
            location = event.get('location')
            summary = event['summary']
            A.append(summary)
            B.append(start.time())
            C.append(end.time())
            D.append(location)
            E.append(start)
            F.append(end)

    output = pd.DataFrame(A, columns=['summary'])
    output['start'] = B
    output['end'] = C
    output['location'] = D
    output['start_full'] = E
    output['end_full'] = F
    output = output.sort_values(by=['start', 'end'])

    G = []
    H = []
    I = []
    J = []
    # Calculate the interval between every events.
    for i in output.index:
        start = output[output.index == i]['start_full']
        interval = start.tolist()[0].replace(tzinfo=None) - dayStart
        end = output[output.index == i]['end_full']
        dayStart = end.tolist()[0]
        G.append(interval.seconds)
        H.append(start)
        I.append(end)
        J.append(dayStart)
#    interval = dayEnd - end.tolist()[0].replace(tzinfo=None)
#    E.append(interval.seconds)
    time_interval = pd.DataFrame(G, columns=['seconds'])
    time_interval['start'] = H
    time_interval['end'] = I
    time_interval['daystart'] = J

    return output, time_interval,desireLocation

output,time_interval,desireLocation = main()
event_lists=[]
for i in range(0, output.shape[0]): 
    if len(str(output.iloc[i]['location']))>4:
        event_lists.append(dict(summary=str(output.iloc[i]['summary']),
                           start=str(output.iloc[i]['start']),
                           end=str(output.iloc[i]['end']),
                           location = str(output.iloc[i]['location'])))
    elif desireLocation:
     event_lists.append(dict(summary=str(output.iloc[i]['summary']),
                            start=str(output.iloc[i]['start']),
                            end=str(output.iloc[i]['end']),
                            location = desireLocation))