import requests

def generate_anisette_headers():
    req = requests.get("http://localhost:6969")

    return req.json()