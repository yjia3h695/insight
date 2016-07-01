import rauth
from api_keys import CONSUMER_KEY, CONSUMER_SECRET, TOKEN, TOKEN_SECRET
import pandas as pd


def yelp_search(address):
    # Define the search parameter for yelp api
    params = {}
    params['term'] = 'fitness'
    params['location'] = address
    # Limit search result within 1.5 miles radius
    params['radius_filter'] = 2415
    # Establish connection with Yelp API
    session = rauth.OAuth1Session(consumer_key=CONSUMER_KEY,
                                  consumer_secret=CONSUMER_SECRET,
                                  access_token=TOKEN,
                                  access_token_secret=TOKEN_SECRET)
    request = session.get('https://api.yelp.com/v2/search', params=params)
    data = request.json()
    session.close()

    busi_id = []
    name = []
    addr = []
    rating = []
    review_count = []
    lat = []
    lng = []
    for business in data['businesses']:
        busi_id.append(business['id'])
        name.append(business['name'])
        addr.append(business['location']['display_address'])
        lat.append(business['location']['coordinate']['latitude'])
        lng.append(business['location']['coordinate']['longitude'])
        rating.append(business['rating'])
        review_count.append(business['review_count'])

    df = pd.DataFrame(busi_id, columns=['busi_id'])
    df['name'] = name
    df['addr'] = addr
    df['rating'] = rating
    df['review_count'] = review_count
    df['lat'] = lat
    df['lng'] = lng

    return df
