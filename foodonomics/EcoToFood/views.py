from django.shortcuts import render
from pprint import pprint
import argparse
import json
import pprint
import sys
import urllib
import urllib2
import oauth2

# Create your views here.
def home(request):
	main();

API_HOST = 'api.yelp.com'
DEFAULT_TERM = 'dinner'
DEFAULT_LOCATION = 'San Francisco, CA'
SEARCH_LIMIT = 10
SEARCH_PATH = '/v2/search/'
BUSINESS_PATH = '/v2/business/'

# OAuth credential placeholders that must be filled in by users.
CONSUMER_KEY = '1GbcTsWyLDWocksmAY608A'
CONSUMER_SECRET = '2IAn50iLysgm4__a49cTvNO9X2M'
TOKEN = 'HVJ5vIeXH__KV4g2nTVoIYRxe_yIuEwj'
TOKEN_SECRET = 'Vc3bYAxJN9HInpoEUOdi-gZJ4vA'

def request(host, path, url_params=None):
    url_params = url_params or {}
    url = 'https://{0}{1}?'.format(host, urllib.quote(path.encode('utf8')))

    consumer = oauth2.Consumer(CONSUMER_KEY, CONSUMER_SECRET)
    oauth_request = oauth2.Request(method="GET", url=url, parameters=url_params)

    oauth_request.update(
        {
            'oauth_nonce': oauth2.generate_nonce(),
            'oauth_timestamp': oauth2.generate_timestamp(),
            'oauth_token': TOKEN,
            'oauth_consumer_key': CONSUMER_KEY
        }
    )
    token = oauth2.Token(TOKEN, TOKEN_SECRET)
    oauth_request.sign_request(oauth2.SignatureMethod_HMAC_SHA1(), consumer, token)
    signed_url = oauth_request.to_url()

    conn = urllib2.urlopen(signed_url, None)
    try:
        response = json.loads(conn.read())
    finally:
        conn.close()

    return response

def search(term=DEFAULT_TERM, location=DEFAULT_LOCATION):
    url_params = {
        'term': term.replace(' ', '+'),
        'location': location.replace(' ', '+'),
        'limit': SEARCH_LIMIT
    }
    result = request(API_HOST, SEARCH_PATH, url_params=url_params)

    return result

def get_business(business_id):
    """Query the Business API by a business ID.
    Args:
        business_id (str): The ID of the business to query.
    Returns:
        dict: The JSON response from the request.
    """
    business_path = BUSINESS_PATH + business_id

    return request(API_HOST, business_path)

def query_api(term, location):
    """Queries the API by the input values from the user.
    Args:
        term (str): The search term to query.
        location (str): The location of the business to query.
    """
    response = search(term, location)

    businesses = response.get('businesses')

    if not businesses:
        print u'No businesses for {0} in {1} found.'.format(term, location)
        return

    business_id = businesses[0]['id']

    print u'{0} businesses found, querying business info for the top result "{1}" ...'.format(
        len(businesses),
        business_id
    )

    response = get_business(business_id)

    print u'Result for business "{0}" found:'.format(business_id)
    return response

def main(request):
    input_values = dict({'term': 'food', 'location': 'London'});

    try:
        context = query_api(input_values['term'], input_values['location'])
        pprint.pprint(context, indent=2)
        return render(request, 'base.html', context['location']['coordinate'])
    except urllib2.HTTPError as error:
        sys.exit('Encountered HTTP error {0}. Abort program.'.format(error.code))

if __name__ == '__main__':
    main()
