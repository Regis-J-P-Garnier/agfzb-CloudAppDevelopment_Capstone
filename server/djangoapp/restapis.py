import requests
import json
from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth
from urllib.parse import urlencode, quote_plus, quote
import os
from dotenv import load_dotenv

project_folder = os.path.expanduser(os.path.dirname(os.path.realpath(__file__)))  # adjust as appropriate
load_dotenv(os.path.join(project_folder, '../djangobackend/.env'))

assert(os.getenv("DEBUG")=="True")
GET_DEALERSHIP_BY_STATE_URL=os.getenv('GET_DEALERSHIP_BY_STATE_URL')
GET_ALL_DEALERSHIP_URL=os.getenv('GET_ALL_DEALERSHIP_URL')
GET_REVIEW_BY_DEALER_URL=os.getenv('GET_REVIEW_BY_DEALER_URL')
POST_REVIEW_URL=os.getenv('POST_REVIEW_URL')
NLU_API_KEY=os.getenv('NLU_API_KEY')
GET_NLU_URL=os.getenv('GET_NLU_URL')
NLU_VERSION =os.getenv('NLU_VERSION')

# for debugging only instead og .ENV
# NON PRESENT EVEN AS COMMENT IN PRODUCTION

# GET_DEALERSHIP_BY_STATE_URL="https://b09a1fd3.eu-gb.apigw.appdomain.cloud/api/dealership"
# GET_ALL_DEALERSHIP_URL="https://b09a1fd3.eu-gb.apigw.appdomain.cloud/api/alldealership"
# GET_REVIEW_BY_DEALER_URL="https://b09a1fd3.eu-gb.apigw.appdomain.cloud/api/review"
# POST_REVIEW_URL="https://b09a1fd3.eu-gb.apigw.appdomain.cloud/api/review"
# NLU_API_KEY="3JRYQBDauu2GkgWjkoffZH7IksttkjR20diV_c9KBMRK"
# GET_NLU_URL="https://api.eu-gb.natural-language-understanding.watson.cloud.ibm.com/instances/2c07214f-0d62-4c52-9bff-6bef76b858dc/v1/analyze"
# NLU_VERSION ='2021-03-25'

def post_request(url, json_payload_dict, api_key=None, headers=None, **kwargs):
    ''' do a POST request '''
    if not (kwargs is None) and not (kwargs == {}):
        if not headers is None:
            headers.update(kwargs)
        else:
            headers=kwargs
    print("POST to {} ".format(url))
    try:# Call get method of requests library with URL and parameters
        if NLU_API_KEY:
            response = requests.post(url,
                                     #auth=HTTPBasicAuth('apikey', api_key),
                                     headers=headers, 
                                     data=json.dumps(json_payload_dict))
        else:
            response = requests.post(url,
                                     headers=headers, 
                                     data=json.dumps(json_payload_dict))
    except: # If any error occurs   
        print("Network exception occurred")  
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    if "error" in json_data.keys():
        pass # TODO error management
    return json_data           

def get_request(url, api_key=None, params=None, **kwargs):
    ''' do a GET request '''
    if not (kwargs is None) and not (kwargs == {}):
        if not params is None:
            params.update(kwargs)
        else:
            params=kwargs
    
    print("GET from {} ".format(url))
    try: # Call get method of requests library with URL and parameters
        if NLU_API_KEY:
            response = requests.get(url, headers={'Content-Type': 'application/json'},
                                    auth=HTTPBasicAuth('apikey', api_key),
                                    params=params)
        else:
            response = requests.get(url, headers={'Content-Type': 'application/json'},
                                    params=params)
    except: # If any error occurs   
        print("Network exception occurred")
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    if "error" in json_data.keys():
        pass # TODO error management
    return json_data        

def post_review_request_to_cf(json_payload_dict):
    return post_request(url=POST_REVIEW_URL, json_payload_dict=json_payload_dict, api_key=NLU_API_KEY, headers={"accept":"application/json","content-type":"application/json"}) 
   
def get_dealers_JSON_parser(json_result):
    ''' parse and convert to model object a GET on dealship database '''
    results = []
    if json_result:
        dealers = json_result["data"] # Get the row list in JSON as dealers
        for dealer in dealers: # For each dealer object
            if (dealer!= {}): # DEBUG : why ???
            # Create a CarDealer object with values in `doc` object
                dealer_obj = CarDealer(address=dealer["address"], city=dealer["city"], full_name=dealer["full_name"],
                                       id=dealer["id"], lat=dealer["lat"], long=dealer["long"],
                                       short_name=dealer["short_name"],
                                       st=dealer["st"], zip=dealer["zip"])
                results.append(dealer_obj)
    return results   

def get_dealers_by_state(url, state, **kwargs):
    ''' call the GET on  '''
    return get_dealers_JSON_parser(get_request(url, state=state))

def get_all_dealers_from_cf(url, **kwargs):
    return get_dealers_JSON_parser(get_request(url))

def get_dealers_from_cf(state=None,**kwargs):
    if state is not None:
        return get_dealers_by_state(GET_DEALERSHIP_BY_STATE_URL, state, **kwargs)
    else :
        print('-> in GET_ALL_DEALERSHIP_URL')
        print(GET_ALL_DEALERSHIP_URL)
        return get_all_dealers_from_cf(GET_ALL_DEALERSHIP_URL, **kwargs)   

def analyze_review_sentiments(review, **kwargs): # review as text or object ?
    """ retireve sentiments on differents items in review and """
    params = {}
    params["text"] = review
    #review #quote_plus(review)
    params["version"] = NLU_VERSION
    params["features"] = 'keywords,entities' # IBM endpoint only support comma separated multivalue : force it !
    params["entities.emotion"] = False
    params["entities.sentiment"] = True
    params["keywords.emotion"] = False
    params["keywords.sentiment"] = True
    # curl -u "apikey:{apikey}"   "{url}/v1/analyze}?version=2021-03-25&url=www.ibm.com&features=keywords,entities&entities.emotion=true&entities.sentiment=true&keywords.emotion=true&keywords.sentiment=true"
    response = get_request(url=GET_NLU_URL, api_key=NLU_API_KEY, params=params)
    # {'usage': {'text_units': 1, 'text_characters': 38, 'features': 2}, 'language': 'en', 
        # 'keywords': [{'text': 'dealer', 'sentiment': {'score': 0.977313, 'label': 'positive'}, 'relevance': 0.87516, 'count': 1}, {'text': 'cars', 'sentiment': {'score': 0.956888, 'label': 'positive'}, 'relevance': 0.74128, 'count': 1}], 'entities': []}
    # TODO : a better algorithm
    score=0.0
    iterations=0
    features=[]
    if 'keywords' in response.keys():
        features.append('keywords')
    if 'entities' in response.keys():
        features.append('entities')
    for list_or_items in features:
        for item in response[list_or_items]:
            try:
                score+=item['sentiment']['score']
                iterations+=1
            except KeyError:
                print("ERROR when retrieving sentiment score from WATSON's response")
                break
    if not iterations == 0:
        score=score/iterations
    else:
        score=None
    return score

def get_reviews_JSON_parser(json_result):
    ''' parse and convert to model object a GET on review database '''
    results = []
    if json_result:
        if not "data" in json_result.keys():
            if "error" in json_result.keys():
                if  404 == json_result["error"]:
                    pass # on empty return 
                else:
                    pass # TODO :error return
        else:
            reviews = json_result["data"] # Get the row list in JSON as dealers
            for review_dict in reviews: # For each dealer object
                if (review_dict != {}): # DEBUG : why ???
                # Create a CarDealer object with values in `doc` object
                    review_obj = DealerReview(review=review_dict["review"], purchase_date=review_dict["purchase_date"], purchase=review_dict["purchase"],
                                           name=review_dict["name"], id=review_dict["id"], dealership=review_dict["dealership"],
                                           car_year=review_dict["car_year"],
                                           car_model=review_dict["car_model"], car_make=review_dict["car_make"])
                    review_obj.sentiment = analyze_review_sentiments(review_obj.review)
                    results.append(review_obj)
                #print(str(review_obj.sentiment)+'->'+review_obj.name)#DEBUG
    return results     
    
def get_dealer_reviews_from_cf(dealer_id=0,**kwargs):
    json_result =  get_request(GET_REVIEW_BY_DEALER_URL, dealerId=dealer_id) 
    result =  get_reviews_JSON_parser(json_result)
    return result

def get_dealer_by_id(dealer_id=None):
            dealership_list= get_dealers_from_cf()
            for dealer in dealership_list:
                if str(dealer.id) == str(dealer_id):
                    return dealer
            return None 
 
# def get_all_dealers_from_cf(url, **kwargs):
#     results = []  
#     json_result = get_request(url) # Call get_request with a URL parameter
#     if json_result:
#         dealers = json_result["data"] # Get the row list in JSON as dealers
#         for dealer in dealers: # For each dealer object
#             if (dealer!= {}): # DEBUG : why ???
#             # Create a CarDealer object with values in `doc` object
#                 dealer_obj = CarDealer(address=dealer["address"], city=dealer["city"], full_name=dealer["full_name"],
#                                        id=dealer["id"], lat=dealer["lat"], long=dealer["long"],
#                                        short_name=dealer["short_name"],
#                                        st=dealer["st"], zip=dealer["zip"])
#                 results.append(dealer_obj)
#     return results


    
    
    
    
    
# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))


# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)


# Create a get_dealers_from_cf method to get dealers from a cloud function
# def get_dealers_from_cf(url, **kwargs):
# - Call get_request() with specified arguments
# - Parse JSON results into a CarDealer object list


# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
# def get_dealer_by_id_from_cf(url, dealerId):
# - Call get_request() with specified arguments
# - Parse JSON results into a DealerView object list


# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# def analyze_review_sentiments(text):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative



