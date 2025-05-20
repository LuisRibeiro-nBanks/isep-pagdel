# IMPORTS..
import requests
from _enums import LocationEnum
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


def get_request_parameters (location):
    return {
        "top": location.value[0],
        "bottom": location.value[1],
        "left": location.value[2],
        "right": location.value[3],
        "env": "row",
        "types": "alerts,traffic,users"
    }


def store_response_as_json (data):    
    int_timestamp = int(time.time())    
    file_name = f"waze_response_{int_timestamp}.json"

    with open(file_name, "w") as f:
        json.dump(data, f, indent=4)

    print(f"Saved the response information to {file_name}")


for location in LocationEnum:
    params = get_request_parameters(location)
    headers = get_request_headers()
    
    print(f"\n\nFetching Waze Data for {location.name}..")
    response = requests.get(WAZE_ENDPOINT, headers=headers, params=params)

    # Just for debugging..    
    print("Status code:", response.status_code)
    
    data = response.json()
    store_response_as_json(data)
    
    alerts = data["alerts"]
    jams = data["jams"]
    users = data["users"]
    
    print("\nFound Information:")
    print(f"- Total Alerts: {len(alerts)}")
    print(f"- Total Users: {len(users)}")
    print(f"- Total Jams: {len(jams)}")