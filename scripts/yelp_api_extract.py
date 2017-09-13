# -*- coding: utf-8 -*-
"""
The code below is adapted from the Yelp Fusion API code sample.

This program demonstrates the capability of the Yelp Fusion API
by using the Search API to query for businesses by a search term and location,
and the Business API to query additional information about the top result
from the search query.

Please refer to http://www.yelp.com/developers/v3/documentation for the API
documentation.
"""
from __future__ import print_function

import argparse
import json
import pprint
import requests
import sys
import urllib
import pandas
import time
import numpy as np
import datetime
import csv


# This client code can run on Python 2.x or 3.x.  Your imports can be
# simpler if you only need one of those.
try:
    # For Python 3.0 and later
    from urllib.error import HTTPError
    from urllib.parse import quote
    from urllib.parse import urlencode
except ImportError:
    # Fall back to Python 2's urllib2 and urllib
    from urllib2 import HTTPError
    from urllib import quote
    from urllib import urlencode


# OAuth credential placeholders that must be filled in by users.
# You can find them on
# https://www.yelp.com/developers/v3/manage_app
CLIENT_ID = "YOUR ID"
CLIENT_SECRET = "YOUR SECRET"


# API constants, you shouldn't have to change these.
API_HOST = 'https://api.yelp.com'
SEARCH_PATH = '/v3/businesses/search'
BUSINESS_PATH = '/v3/businesses/'  # Business ID will come after slash.
TOKEN_PATH = '/oauth2/token'
GRANT_TYPE = 'client_credentials'


# Defaults for our simple example.
DEFAULT_TERM = 'restaurant'
DEFAULT_LOCATION = 'Houston, TX'
SEARCH_LIMIT = 50
OFFSET = 0

# list to save all json results.
l=[]


def obtain_bearer_token(host, path):
    """Given a bearer token, send a GET request to the API.

    Args:
        host (str): The domain host of the API.
        path (str): The path of the API after the domain.
        url_params (dict): An optional set of query parameters in the request.

    Returns:
        str: OAuth bearer token, obtained using client_id and client_secret.

    Raises:
        HTTPError: An error occurs from the HTTP request.
    """
    url = '{0}{1}'.format(host, quote(path.encode('utf8')))
    assert CLIENT_ID, "Please supply your client_id."
    assert CLIENT_SECRET, "Please supply your client_secret."
    data = urlencode({
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'grant_type': GRANT_TYPE,
    })
    headers = {
        'content-type': 'application/x-www-form-urlencoded',
    }
    response = requests.request('POST', url, data=data, headers=headers)
    bearer_token = response.json()['access_token']
    return bearer_token


def request(host, path, bearer_token, url_params=None):
    """Given a bearer token, send a GET request to the API.

    Args:
        host (str): The domain host of the API.
        path (str): The path of the API after the domain.
        bearer_token (str): OAuth bearer token, obtained using client_id and client_secret.
        url_params (dict): An optional set of query parameters in the request.

    Returns:
        dict: The JSON response from the request.

    Raises:
        HTTPError: An error occurs from the HTTP request.
    """
    url_params = url_params or {}
    url = '{0}{1}'.format(host, quote(path.encode('utf8')))
    headers = {
        'Authorization': 'Bearer %s' % bearer_token,
    }

    print(u'Querying {0} ...'.format(url))

    response = requests.request('GET', url, headers=headers, params=url_params)

    return response.json()


def search(bearer_token, term, location):
    """Query the Search API by a search term and location.

    Args:
        term (str): The search term passed to the API.
        location (str): The search location passed to the API.

    Returns:
        dict: The JSON response from the request.
    """

    url_params = {
        'term': term.replace(' ', '+'),
        'location': location.replace(' ', '+'),
        'limit': SEARCH_LIMIT,
        'offset': OFFSET
    }
    return request(API_HOST, SEARCH_PATH, bearer_token, url_params=url_params)


def get_business(bearer_token, business_id):
    """Query the Business API by a business ID.

    Args:
        business_id (str): The ID of the business to query.

    Returns:
        dict: The JSON response from the request.
    """
    business_path = BUSINESS_PATH + business_id

    return request(API_HOST, business_path, bearer_token)

def get_business_review(bearer_token, business_id):
    """Query the Review API by a business ID.

    Args:
        business_id (str): The ID of the business to query.

    Returns:
        dict: The JSON response from the request.
    """
    review_path = BUSINESS_PATH + business_id + '/reviews'

    return request(API_HOST, review_path, bearer_token)


def query_api(term, location):
    """Queries the API by the input values from the user.

    Args:
        term (str): The search term to query.
        location (str): The location of the business to query.
    """
    bearer_token = obtain_bearer_token(API_HOST, TOKEN_PATH)

    response = search(bearer_token, term, location)

    businesses = response.get('businesses')

    if not businesses:
        print(u'No businesses for {0} in {1} found.'.format(term, location))
        return

    for b in businesses: 
        business_id = b['id']
    
    # this part is to get business details.
#        print(u'{0} businesses found, querying business info ' \
#            'for the top result "{1}" ...'.format(
#                len(businesses), business_id))
#        response = get_business(bearer_token, business_id)
#        l.append(response)

        # This part is to get review details.        

        print(u'{0} businesses found, querying review info ' \
            'for the top result "{1}" ...'.format(
                len(businesses), business_id))
        response = get_business_review(bearer_token, business_id)
        temp =  business_id +","+str(response)
        l.append(temp)



parser = argparse.ArgumentParser()

parser.add_argument('-q', '--term', dest='term', default=DEFAULT_TERM,
                    type=str, help='Search term (default: %(default)s)')
parser.add_argument('-l', '--location', dest='location',
                    default=DEFAULT_LOCATION, type=str,
                    help='Search location (default: %(default)s)')

input_values = parser.parse_args()

# known issue: if the api returns till the end but the offset is still less than the limit,
# it won't automatically break. You will need to manually interrupt. (To be fixed in the future)
while OFFSET < 500:
    try:
        query_api(input_values.term, input_values.location)
    except HTTPError as error:
        sys.exit(
            'Encountered HTTP error {0} on {1}:\n {2}\nAbort program.'.format(
                error.code,
                error.url,
                error.read(),
            )
        )
    time.sleep(30.0)
    OFFSET = OFFSET + 50

#save list (utf8 encoding)
today = datetime.datetime.today()
outputname = "json_restaurant_review_"+str(today).replace(':','-')+".csv"
with open(outputname, 'wb') as f:
    for item in l:
        f.write(item.encode('utf-8'))
        f.write("\n")
