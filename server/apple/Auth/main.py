import os
import json

def getAuth():
    with open(os.path.join(os.path.dirname(__file__), 'apple_secrets.json'), 'r') as f:
        j = json.load(f)
        return j['dsid'], j['searchPartyToken']