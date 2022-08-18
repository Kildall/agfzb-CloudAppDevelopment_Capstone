from operator import contains
from unittest import result
import requests
import json
from requests.auth import HTTPBasicAuth
from .models import CarDealer, DealerReview



# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))

def get_request(url, **kwargs):
    json_data = {}
    if "api_key" in kwargs:
        params = dict()
        params["text"] = kwargs["text"]
        params["version"] = kwargs["version"]
        params["features"] = kwargs["features"]
        response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
                                            auth=HTTPBasicAuth('apikey', kwargs["api_key"]))
        json_data = json.loads(response.text)
        return json_data
    else:
        print("GET from {} ".format(url))
        try:
            response = requests.get(url, headers={'Content-Type': 'application/json'},
                                        params=kwargs)
        except:
            # If any error occurs
            print("Network exception occurred")
        status_code = response.status_code
        print("With status {} ".format(status_code))
        if(response.status_code is not 200):
            return {}
        json_data = json.loads(response.text)
        return json_data

def post_request(url, payload, **kwargs):
    json_data = {}
    print("POST to {} with params {}".format(url, kwargs))
    try:
        response = requests.post(url, params=kwargs, json=payload)
    except:
        # If any error occurs
        print("Network exception occurred")
    status_code = response.status_code
    print("With status {} ".format(status_code))
    if(response.status_code is not 200):
        return {}
    json_data = json.loads(response.text)
    return json_data



# Create a get_dealers_from_cf method to get dealers from a cloud function
# def get_dealers_from_cf(url, **kwargs):
# - Call get_request() with specified arguments
# - Parse JSON results into a CarDealer object list
def get_dealers_from_cf(url, **kwargs):
    results = []
    
    # Call get_request with a URL parameter
    json_result = get_request(url)
    if json_result:
        # For each dealer object
        for dealer in json_result['documents']:
            # Get its content in `doc` object
            dealer_doc = dealer["doc"]
            if dealer_doc["_id"].__contains__("index"):
                continue
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                   id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                   short_name=dealer_doc["short_name"],
                                   st=dealer_doc["st"], zip=dealer_doc["zip"])
            results.append(dealer_obj)
    return results

def get_dealers_by_param(url, **kwargs):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url, **kwargs)
    if json_result['documents']:
        # Get its content in `doc` object
        for dealer_doc in json_result['documents']:
            if dealer_doc["_id"].__contains__("index"):
                return {}
                # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                    id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                    short_name=dealer_doc["short_name"],
                                    st=dealer_doc["st"], zip=dealer_doc["zip"])
        results.append(dealer_obj)
    return results


# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
# def get_dealer_by_id_from_cf(url, dealerId):
# - Call get_request() with specified arguments
# - Parse JSON results into a DealerView object list
def get_dealer_review_from_cf(url, **kwargs):
    results = []
    if 'id' not in kwargs:
        return None
    # Call get_request with a URL parameter
    json_result = get_request(url, **kwargs)
    if json_result:
        # For each dealer object
        for review in json_result['documents']['docs']:
            # Get its content in `doc` object
            review_doc = review
            if review_doc["_id"].__contains__("design"):
                continue
            # Create a CarDealer object with values in `doc` object
            review_obj = DealerReview(dealership=review_doc["dealership"], purchase=review_doc["purchase"], name=review_doc["name"],
                                   review=review_doc["review"], purchase_date=review_doc.get("purchase_date"), car_make=review_doc.get("car_make"),
                                   car_model=review_doc.get("car_model"),
                                   car_year=review_doc.get("car_year"))
            results.append(review_obj)
    return results




# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# def analyze_review_sentiments(text):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative
def analyze_review_sentiments(text):
    result = {}
    if not text:
        return result
    args = {
        'text': text,
        'version': '2022-04-07',
        'api_key': '',
        'features': {
            'sentiment': True
        }
    }
    json_result = get_request('https://api.us-east.natural-language-understanding.watson.cloud.ibm.com/instances/522fa0fa-722c-4d2e-8808-3813db121f65/v1/analyze', **args)
    if 'error' not in json_result and json_result:
        return json_result['sentiment']['document']['label'].capitalize()
    else:
        return ""


def post_review(url, review, **kwargs):
    results = []
    datos = {"review": json.loads(json.dumps(review.__dict__, default=str))}
    post_request(url,payload=datos,**kwargs)
    return results