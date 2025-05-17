import requests

url = "https://www.waze.com/live-map/api/georss"

params = {
    "top": "41.17225860635491",
    "bottom": "41.14356652706814",
    "left": "-8.688709259033205",
    "right": "-8.569438934326174",
    "env": "row",
    "types": "alerts,traffic,users"
}

headers = {
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
    "referer": "https://www.waze.com/pt-PT/live-map/"
}

response = requests.get(url, headers=headers, params=params)

# Print response status and JSON content (or XML/text depending on the actual API)
print("Status code:", response.status_code)
print("Response:")
print(response.text)
