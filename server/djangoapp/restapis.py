import requests
import json
from .models import CarDealer
from requests.auth import HTTPBasicAuth


GET_DEALERSHIP_BY_STATE_URL="https://b09a1fd3.eu-gb.apigw.appdomain.cloud/api/dealership"
GET_ALL_DEALERSHIP_URL="https://b09a1fd3.eu-gb.apigw.appdomain.cloud/api/alldealership"
GET_REVIEW_BY_DEALER_URL="https://b09a1fd3.eu-gb.apigw.appdomain.cloud/api/review"
POST_REVIEW_URL="https://b09a1fd3.eu-gb.apigw.appdomain.cloud/api/review"

def get_request(url, **kwargs):
    ''' do a GET request '''
    print(kwargs)
    print("GET from {} ".format(url))
    try: # Call get method of requests library with URL and parameters
        response = requests.get(url, headers={'Content-Type': 'application/json'},
                                    params=kwargs)
    except: # If any error occurs   
        print("Network exception occurred")
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    if "error" in json_data.keys():
        pass # TODO error management
    return json_data        

    
def get_dealers_JSON_parser(json_result):
    ''' parse and convert to model object a GET on dealship database '''
    results = []
    if json_result:
        print(json_result.keys())
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

def get_reviews_JSON_parser(json_result):
    ''' parse and convert to model object a GET on review database '''
    results = []
    if json_result:
        reviews = json_result["data"] # Get the row list in JSON as dealers
        for review in reviews: # For each dealer object
            if (review != {}): # DEBUG : why ???
            # Create a CarDealer object with values in `doc` object
                review_obj = CarDealer(review=review["review"], purchase_date=review["purchase_date"], purchase=review["purchase"],
                                       name=review["name"], id=review["id"], dealership=review["dealership"],
                                       car_year=review["car_year"],
                                       car_model=review["car_model"], car_make=review["car_make"])
                results.append(review_obj)
    return results     
    
    

def get_dealer_reviews_from_cf(dealer_id=0,**kwargs):
    json_result =  get_request(GET_REVIEW_BY_DEALER_URL, dealerId=dealer_id)   
    return get_reviews_JSON_parser(json_result)

 
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



