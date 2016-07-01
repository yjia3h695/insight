import datetime
from pyrfc3339 import parse
import pandas as pd
import pytz


def find_interval(output, dayStart, dayEnd):
    G = []
    H = [0]
    I = [0]
    J = [0]
    # Calculate the interval between every events.
    for i in output.index:
        start = output[output.index == i]['start_full']
        interval = start.tolist()[0] - dayStart
        end = output[output.index == i]['end_full']
        dayStart = end.tolist()[0]
        G.append(interval.seconds)
        H.append(start)
        I.append(end)
        J.append(dayStart)
    interval = dayEnd - end.tolist()[0]
    G.append(interval.seconds)
    time_interval = pd.DataFrame(G, columns=['seconds'])
    time_interval['start'] = H
    time_interval['end'] = I
    time_interval['daystart'] = J
    return time_interval


def read_calendar(service, start_hour=7, start_min=0,
                  end_hour=20, end_min=0, prime=0):

    eastern = pytz.timezone('US/Eastern')
    # Find curent local time
    local_now = datetime.datetime.now()
    # Limit events happend tomorrow
    now_reset = eastern.localize(local_now.replace(hour=23, minute=59,
                                                   second=0, microsecond=0))
    now = now_reset.isoformat()
    tomorrow = (now_reset + datetime.timedelta(days=1)).isoformat()
    # Limit the time range to schedule your fitness
    get_tomorrow = datetime.datetime.today() + datetime.timedelta(days=1)
    dayStart = eastern.localize(get_tomorrow.replace(hour=start_hour,
                                                     minute=start_min,
                                                     second=0, microsecond=0))
    dayEnd = eastern.localize(get_tomorrow.replace(hour=end_hour,
                                                   minute=end_min,
                                                   second=0, microsecond=0))
    if prime == 0:
        # Getting your calender lists
        calIDlistResults = service.calendarList().list().execute()
        calIDlists = calIDlistResults.get('items', [])

        A = []
        B = []
        C = []
        D = []
        E = []
        F = []
        G = []

        # Iterate through all avaliable calender
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
                time_dif = (start - end).seconds
                A.append(summary)
                B.append(start.time())
                C.append(end.time())
                D.append(location)
                E.append(start)
                F.append(end)
                G.append(time_dif)

        output = pd.DataFrame(A, columns=['summary'])
        output['start'] = B
        output['end'] = C
        output['location'] = D
        output['start_full'] = E
        output['end_full'] = F
        output['time_dif'] = G
        output = output.sort_values(by=['start', 'end'])

        return output, find_interval(output, dayStart, dayEnd)

    else:

        A = []
        B = []
        C = []
        D = []
        E = []
        F = []
        G = []

        eventsResult = service.events().list(calendarId='primary', timeMin=now,
                                             timeMax=tomorrow).execute()
        events = eventsResult.get('items', [])

        for event in events:
            start = parse(event['start'].get('dateTime'))
            end = parse(event['end'].get('dateTime'))
            location = event.get('location')
            summary = event['summary']
            time_dif = (start - end).seconds
            A.append(summary)
            B.append(start.time())
            C.append(end.time())
            D.append(location)
            E.append(start)
            F.append(end)
            G.append(time_dif)

        output = pd.DataFrame(A, columns=['summary'])
        output['start'] = B
        output['end'] = C
        output['location'] = D
        output['start_full'] = E
        output['end_full'] = F
        output['time_dif'] = G
        output = output.sort_values(by=['start', 'end'])

        return output, find_interval(output, dayStart, dayEnd)
