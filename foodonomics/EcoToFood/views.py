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
SEARCH_LIMIT = 20
SEARCH_PATH = '/v2/search/'
BUSINESS_PATH = '/v2/business/'

# OAuth credential placeholders that must be filled in by users.
CONSUMER_KEY = '1GbcTsWyLDWocksmAY608A'
CONSUMER_SECRET = '2IAn50iLysgm4__a49cTvNO9X2M'
TOKEN = 'HVJ5vIeXH__KV4g2nTVoIYRxe_yIuEwj'
TOKEN_SECRET = 'Vc3bYAxJN9HInpoEUOdi-gZJ4vA'

def londonPopulation():
	#data from wikipedia
	Population = {};
	Population["Islington"] = 14,735
	Population["Tower Hamlets"] = 14,201
	Population["Hackney"] = 13,850
	Population["Kensington and Chelsea"] = 13,016
	Population["Lambeth"] = 11,786
	Population["Hammersmith and Fulham"] = 11,148
	Population["Westminster"] = 11,109
	Population["Camden"] = 10,675
	Population["Southwark"] = 10,432
	Population["Wandsworth"] = 9,181
	Population["Newham"] = 9,009
	Population["Haringey"] = 8,918
	Population["Lewisham"] = 8,341
	Population["Brent"] = 7,460
	Population["Waltham Forest"] = 6,872
	Population["Ealing"] = 6,109
	Population["Greenwich"] = 5,717
	Population["Barking and Dagenham"] = 5,508
	Population["Merton"] = 5,356
	Population["Redbridge"] = 5,233
	Population["Harrow"] = 4,920
	Population["Hounslow"] = 4,742
	Population["Kingston upon Thames"] = 4,593
	Population["Sutton"] = 4,503
	Population["Croydon"] = 4,373
	Population["Barnet"] = 4,309
	Population["Enfield"] = 4,007
	Population["Bexley"] = 3,932
	Population["Richmond upon Thames"] = 3,396
	Population["City of London"] = 2,691
	Population["Hillingdon"] = 2,523
	Population["Havering"] = 2,196
	Population["Bromley"] = 2,142
	return Population

def request(host, path, url_params=None):
    url_params = url_params or {}
    url = 'https://{0}{1}?'.format(host, urllib.quote(path.encode('utf8')))
    print url

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
    responseList = []
    for i in businesses:
    	business_id = i['id']
    	response = get_business(business_id)
    	responseList.append(response)

    #print u'Result for business "{0}" found:'.format(business_id)
    return responseList

def main(request):
    """
    input_values = dict({'term': 'coffee & tea', 'location': 'Vegesack'});
    context = {}
    try:
    	context['listOfResponses'] = [];
    	LondonRegions = ["Barking and Dagenham", "Barnet", "Bexley", "Brent", "Bromley", "Camden", "Croydon", "Ealing", "Enfield", "Greenwich", "Hackney", "Hammersmith and Fulham", "Haringey", "Harrow", "Havering", "Hillingdon", "Hounslow", "Islington", "Kensington and Chelsea", "Kingston upon Thames", "Lambeth", "Lewisham", "Merton", "Newham", "Redbridge", "Richmond upon Thames", "Southwark", "Sutton", "Tower Hamlets", "Waltham Forest", "Wandsworth", "Westminster, London"];
    	for i in LondonRegions:
        	context['listOfResponses'] = context['listOfResponses'] + query_api(input_values['term'], i)
        with open('coffee.json', 'w') as fp:
            json.dump(context, fp)
        return render(request, 'base.html', context)
    except urllib2.HTTPError as error:
        sys.exit('Encountered HTTP error {0}. Abort program.'.format(error.code))
    """
    r = open('restaurant.json')
    restaurant_dict = json.load(r)
    c = open('coffee.json')
    coffee_dict = json.load(c)
    context = {}
    context['restaurant'] = restaurant_dict
    context['coffee'] = coffee_dict
    return render(request, 'base.html', context)
    #"""
if __name__ == '__main__':
    main()
