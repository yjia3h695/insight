from weather import get_forcast
import pickle
from get_location import get_distance, get_box, from_latlng
import pandas as pd
from yelp_search import yelp_search
from stravaapi import list_running_path


def predict_outdoor(address):
    # Predict whether the weather good for running ourside or not.
    weather = get_forcast(address)
    test = weather[['mean_tempf', 'max_tempf', 'mean_dew_pointf',
                    'mean_hum', 'mean_wind_speed',
                    'wind_dir_degrees', 'mean_visibility_miles']]
    X_test = test.values
    model = pickle.load(open
                        ("/home/yanxin/flask/aws3/app/model/model.p", "rb"))
    y = model.predict(X_test)
    return y


def predict_segments(address):
    # Search for routes based on outdoor/indoor preference
    outdoor_flag = predict_outdoor(address)
    # Outdoor
    if outdoor_flag == 1:
        suggest = """Great weather for running outside,
                     bring your running shoes!"""
        box = get_box(address)
        segments = list_running_path(box)
    # Indoor
    else:
        suggest = """Not a great day for running outside,
                     Lets go to fitness center."""
        segments = yelp_search(address)
    return segments, suggest


def predict_segment_info(address):
    time_array = []
    segment_id = []
    distance_array = []
    latgroup = []
    lnggroup = []
    names = []
    urls = []
    segments, suggest = predict_segments(address)
    if suggest == """Great weather for running outside,
                     bring your running shoes!""":
        for segment in segments.values:
            try:
                seg_id = segment[0]
                seg_name = segment[1]
                s_lat = segment[2]
                s_end = segment[3]
                seg_url = segment[4]
                end_address, e_city, e_state = from_latlng(s_lat, s_end)
                dista, durat = get_distance(address, end_address)
                time_array.append(durat / 60)
                segment_id.append(seg_id)
                distance_array.append(dista)
                latgroup.append(s_lat)
                lnggroup.append(s_end)
                names.append(seg_name)
                urls.append(seg_url)
            except:
                pass
        df = pd.DataFrame(segment_id, columns=['segment_id'])
        df['address'] = end_address
        df['total_time'] = time_array
        df['distance'] = distance_array
        df['lat'] = latgroup
        df['lng'] = lnggroup
        df['name'] = names
        df['url'] = urls
        df = df.sort_values(by='distance')
        return df, suggest

    elif suggest == """Not a great day for running outside,
                     Lets go to fitness center.""":
        de = segments
        for business in suggest.values:
            business_address = business[2]
            dista, durat = get_distance(address, business_address)
            total_time = int(durat) / 60
            time_array.append(total_time)
            distance_array.append(dista)
        de['total_time'] = time_array
        de['distance'] = distance_array
        de = de.sort_values(by='distance')
        return de, suggest
