import requests
from django.conf import settings

def godaddy_api_request(endpoint, method="GET", params=None, data=None):
    base_url = settings.GODADDY_BASE_URL
    api_key = settings.GODADDY_API["api_key"]
    api_secret = settings.GODADDY_API["api_secret"]

    headers = {
        "Authorization": f"sso-key {api_key}:{api_secret}",
        "Content-Type": "application/json",
    }

    url = f"{base_url}{endpoint}"

    if method == "GET":
        response = requests.get(url, headers=headers, params=params)
    elif method == "POST":
        response = requests.post(url, headers=headers, json=data)
    else:
        raise ValueError("Unsupported HTTP method")

    response.raise_for_status()
    return response.json()
