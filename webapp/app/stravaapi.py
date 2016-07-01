# -*- coding: utf-8 -*-
"""
Created on Wed Jun 15 08:09:26 2016

@author: yanxin
"""
from stravalib.client import Client
from api_keys import STRAVA_TOKEN
import pandas as pd

client = Client(STRAVA_TOKEN)


def find_segments(box):
    segment_ids = []
    segments = client.explore_segments(bounds=box, activity_type='running')
    for segment in segments:
        seg_id = segment.id
        segment_ids.append(seg_id)
    return segment_ids


def retrieve_segment(s_id):
    segment = client.get_segment(segment_id=s_id)
    name = segment.name
    lat = segment.start_latitude
    lng = segment.start_longitude
    ids = segment.id
    url = 'https://www.strava.com/segments/' + str(ids)
    return ids, name, lat, lng, url


def list_running_path(box):
    name = []
    lat = []
    lng = []
    ids = []
    url = []
    segment_ids = find_segments(box)
    for seg_id in segment_ids:
        s_id, s_name, s_lat, s_lng, s_url = retrieve_segment(seg_id)
        ids.append(s_id)
        name.append(s_name)
        lat.append(s_lat)
        lng.append(s_lng)
        url.append(s_url)
    df = pd.DataFrame(ids, columns=['segment_id'])
    df['name'] = name
    df['start_latitude'] = lat
    df['start_longitude'] = lng
    df['url'] = url

    return df
