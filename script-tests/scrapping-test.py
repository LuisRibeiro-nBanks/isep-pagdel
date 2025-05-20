# IMPORTS..
import requests
from bounding_box_enum import BoundingBoxEnum
import time
import json


# To set up the environment..
WAZE_ENDPOINT = "https://www.waze.com/live-map/api/georss"
WAZE_REFERER = "https://www.waze.com/pt-PT/live-map/"


def get_request_headers ():
    return {
        "accept": "application/json, text/plain, */*",
        "accept-language": "en-US,en;q=0.9",
        "if-none-match": 'W/"5c51e-i4mHBr9ol8jRlJ88PR74juLKxRM"',
        "priority": "u=1, i",
        "sec-ch-ua": '"Not.A/Brand";v="99", "Chromium";v="136"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "referer": WAZE_REFERER
    }

def get_request_parameters (bouding_box):
    return {
        "top": bouding_box.value[0],
        "bottom": bouding_box.value[1],
        "left": bouding_box.value[2],
        "right": bouding_box.value[3],
        "env": "row",
        "types": "alerts,traffic,users"
    }
    

def store_response_as_json (response):
    # Get the response body as JSON..
    data = response.json()
    
    int_timestamp = int(time.time())    
    file_name = f"response_{int_timestamp}.json"

    with open(file_name, "w") as f:
        json.dump(data, f, indent=4)

    print(f"Saved the response information to {file_name}")


for bounding_box in BoundingBoxEnum:
    params = get_request_parameters(bounding_box)
    headers = get_request_headers()
    
    print(f"\n\nFetching Waze Data for {bounding_box.name}..")
    response = requests.get(WAZE_ENDPOINT, headers=headers, params=params)

    # Just for debugging..    
    print("Status code:", response.status_code)
    store_response_as_json(response)