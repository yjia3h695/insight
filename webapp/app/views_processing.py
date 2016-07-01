def process_event(output, prefer_address):
    # Read in the upcoming events.
    event_lists = []
    for i in range(0, output.shape[0]):
        # Check if user have valid address in events
        # description, which later used to determine user locations
        if len(str(output.iloc[i]['location'])) > 4:
            event_lists.append(dict(summary=str(output.iloc[i]['summary']),
                                    start=(output.iloc[i]['start']),
                                    end=(output.iloc[i]['end']),
                                    location=str(
                                        output.iloc[i]['location']),
                                    time_dif=(output.iloc[i]['time_dif'])))
        else:
            event_lists.append(dict(summary=str(output.iloc[i]['summary']),
                                    start=(output.iloc[i]['start']),
                                    end=(output.iloc[i]['end']),
                                    location=prefer_address,
                                    time_dif=(output.iloc[i]['time_dif'])))
    return event_lists


def process_interval(interval):
    time_interval = []
    for t in range(0, interval.shape[0]):
        time_interval.append(dict(interval=interval.iloc[t]['seconds'],
                                  start=interval.iloc[t]['start'],
                                  end=interval.iloc[t]['end'],
                                  daytart=interval.iloc[t]['daystart']))
    return time_interval
