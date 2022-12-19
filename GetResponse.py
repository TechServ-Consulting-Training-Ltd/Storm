import requests
import json

def get_response(url, params = None):
    return requests.get(url, params).json()['features']