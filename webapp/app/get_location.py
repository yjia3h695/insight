import requests
from api_keys import GOOGLE_KEY

geo_s = 'https://maps.googleapis.com/maps/api/geocode/json'
distance_s = 'https://maps.googleapis.com/maps/api/distancematrix/json'
place_s = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json'


def from_address(address):
    # Geocoding an address
    param = {'address': address, 'key': GOOGLE_KEY}
    response = requests.get(geo_s, params=param)
    json_dict = response.json()
    lat = json_dict['results'][0]['geometry']['location']['lat']
    lng = json_dict['results'][0]['geometry']['location']['lng']
    return lat, lng


def from_latlng(lat, lng):
    latlng = str(lat) + ',' + str(lng)
    # Geocoding an lat,lng
    param = {'latlng': latlng, 'key': GOOGLE_KEY}
    response = requests.get(geo_s, params=param)
    json_dict = response.json()
    address = json_dict['results'][0]['formatted_address']
    city = json_dict['results'][0]['address_components'][3]['short_name']
    state = json_dict['results'][0]['address_components'][5]['short_name']
    if state == 'US':
        city = json_dict['results'][0]['address_components'][2]['short_name']
        state = json_dict['results'][0]['address_components'][4]['short_name']
    return address, city, state


def get_box(address):
    # Giving a address, find the region of the city, state
    lat, lng, = from_address(address)
    addr, city, state = from_latlng(lat, lng)
    city_state = city + ',' + state
    param = {'address': city_state, 'key': GOOGLE_KEY}
    response = requests.get(geo_s, params=param)
    json_dict = response.json()
    ne_lat = json_dict['results'][0]['geometry'][
        'viewport']['northeast']['lat']
    ne_lng = json_dict['results'][0]['geometry'][
        'viewport']['northeast']['lng']
    sw_lat = json_dict['results'][0]['geometry'][
        'viewport']['southwest']['lat']
    sw_lng = json_dict['results'][0]['geometry'][
        'viewport']['southwest']['lng']
    return (sw_lat, sw_lng, ne_lat, ne_lng)


def get_distance(s_address, e_address):
    # Calculate the distance between two addresses
    param = {'origins': s_address, 'destinations': e_address,
             'key': GOOGLE_KEY, 'mode': 'walking'}
    response = requests.get(distance_s, params=param)
    json_dict = response.json()
    dist = json_dict['rows'][0]['elements'][0]['distance']['value']
    dura = json_dict['rows'][0]['elements'][0]['duration']['value']
    return dist, dura
