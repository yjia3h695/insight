def segment_lists(segments):
    segment_lists = []
    # Case where weather good for run, search for strava data
    if segments.shape[1] == 8:
        for n in range(0, segments.shape[0]):
            distance = (segments.iloc[n]['distance']) / 1610.0
            distance = int((distance * 100) + 0.5) / 100.0
            segment_lists.append(dict(name=str(segments.iloc[n]['name']),
                                      lat=float(segments.iloc[n]['lat']),
                                      lng=float(segments.iloc[n]['lng']),
                                      url=str(segments.iloc[n]['url']),
                                      travel_time=str(
                                      (segments.iloc[n]['total_time'])),
                                      distance=str(distance)))
    # Case where weather bad for run, search for yelp data
    elif segments.shape[1] == 9:
        for k in range(0, segments.shape[0]):
            distance = (segments.iloc[k]['distance']) / 1610.0
            # Transfer from meters to miles with double decimal
            distance = int((distance * 100) + 0.5) / 100.0
            segment_lists.append(dict(name=str(segments.iloc[k]['name']),
                                      lat=str(segments.iloc[k]['lat']),
                                      lng=str(segments.iloc[k]['lng']),
                                      travel_time=str(
                                      (segments.iloc[k]['total_time'])),
                                      address=str(segments.iloc[k]['addr']),
                                      rating=str(segments.iloc[k]['rating']),
                                      review_count=str(segments.iloc[k][
                                                       'review_count']),
                                      distance=str(distance)))
    return segment_lists
