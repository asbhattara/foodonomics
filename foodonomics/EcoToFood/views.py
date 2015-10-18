from django.shortcuts import render
from pprint import pprint
import argparse
import json
import pprint
import sys
import urllib
import urllib2
import oauth2


def home(request):
    context = {}
    
    if request.method == 'GET':
        return render(request, 'home.html', context)

    mapParameters = {}
    mapParameters[1] = numberOfRestaurants
    mapParameters[2] = numberOfCoffeeShops
    mapParameters[3] = populationDensity
    mapParameters[4] = propertyPrice
    mapParameters[5] = studentPopulationDensity
    mapParameters[6] = educationalInstitutes
    mapParameters[7] = investmentCompanies

    allowedParameters = []
    busType =  request.POST.get("type", "")
    if busType == 1:
        allowedParameters = [4,6,7]
    elif busType == 2:
        allowedParameters = [1,3,4]
    else:
        allowedParameters = [1,4,5]

    selected_parameters = some_var = request.POST.getlist('checks')

    if selected_parameters in allowedParameters:
        print "alles gut"
    else:
        "nicht so gut"

    context = {}
    for i in selected_parameters:
        if i == 1:
            r = open('restaurant.json')
            restaurant_dict = json.load(r)
            context['restaurant'] = restaurant_dict
        elif i == 2:
            c = open('coffee.json')
            coffee_dict = json.load(c)
            context['coffee'] = coffee_dict
        elif i == 3:
            print populationDensity
        elif i == 4:
            print propertyPrice
        elif i == 5:
            print studentPopulationDensity
        elif i == 6:
            print educationalInstitutes
        elif i == 7:
            print investmentCompanies
    
    
    return render(request, 'result.html', context)


#londonPopulation()





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
    Population = {}
    Population["Islington"] = 14735
    Population["Tower Hamlets"] = 14201
    Population["Hackney"] = 13850
    Population["Kensington and Chelsea"] = 13016
    Population["Lambeth"] = 11786
    Population["Hammersmith and Fulham"] = 11148
    Population["Westminster"] = 11109
    Population["Camden"] = 10675
    Population["Southwark"] = 10432
    Population["Wandsworth"] = 9181
    Population["Newham"] = 9009
    Population["Haringey"] = 8918
    Population["Lewisham"] = 8341
    Population["Brent"] = 7460
    Population["Waltham Forest"] = 6872
    Population["Ealing"] = 6109
    Population["Greenwich"] = 5717
    Population["Barking and Dagenham"] = 5508
    Population["Merton"] = 5356
    Population["Redbridge"] = 5233
    Population["Harrow"] = 4920
    Population["Hounslow"] = 4742
    Population["Kingston upon Thames"] = 4593
    Population["Sutton"] = 4503
    Population["Croydon"] = 4373
    Population["Barnet"] = 4309
    Population["Enfield"] = 4007
    Population["Bexley"] = 3932
    Population["Richmond upon Thames"] = 3396
    Population["City of London"] = 2691
    Population["Hillingdon"] = 2523
    Population["Havering"] = 2196
    Population["Bromley"] = 2142
    with open('population.json', 'w') as fp:
        json.dump(Population, fp)
    render(request, 'base.html', Population)

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
    return render(request, 'testApi.html', context)
    #"""
if __name__ == '__main__':
    main()
