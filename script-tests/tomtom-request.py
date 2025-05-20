# IMPORTS..
import requests
from _enums import LocationEnum
import time
import json

# To set up the environment..
TOM_TOM_LIVE_ENDPOINT = "https://www.tomtom.com/traffic-index/api/live-traffic/"
TOM_TOM_HISTORIC_ENDPOINT = "https://www.tomtom.com/traffic-index/_next/data/D9tLKRxb7tKfb5wlrfR3u/porto-traffic.json"


def get_request_parameters (code):
    return {
        "cityId": code
    }
    

def get_request_headers ():
    return {
        "referer": "https://www.tomtom.com/traffic-index/porto-traffic/"
    }
    

def store_response_as_json (data, type):    
    int_timestamp = int(time.time())    
    file_name = f"tomtom_{type}_response_{int_timestamp}.json"

    with open(file_name, "w") as f:
        json.dump(data, f, indent=4)

    print(f"Saved the response information to {file_name}")



for location in LocationEnum:
    code = location.value[4]
    params = get_request_parameters(code)
    headers = get_request_headers()
    
    print(f"\n\nFetching TOM TOM Data for {location.name}..")
    response = requests.get(TOM_TOM_LIVE_ENDPOINT, headers=headers, params=params)
    
    print("Status code:", response.status_code)
    data = response.json()
    store_response_as_json(data, "live")
    
    url = f"{TOM_TOM_HISTORIC_ENDPOINT}?cityOrCountry={location.name.lower()}-traffic"
    response = requests.get(url)
    
    print("Status code:", response.status_code)
    data = response.json()
    store_response_as_json(data, "historic")
    