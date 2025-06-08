import os
import json
import gpsoauth
from google.Auth.fcm_receiver import FcmReceiver
from google.Auth.token_cache import get_cached_value_or_set
from binascii import unhexlify

def get_shared_key() -> bytes:
    with open(os.path.join(os.path.dirname(__file__), 'google_secrets.json'), 'r') as f:
        data = json.load(f)
        return unhexlify(data["shared_key"])
def get_aas_token():
    with open(os.path.join(os.path.dirname(__file__), 'google_secrets.json'), 'r') as f:
        data = json.load(f)
        return data["aas_token"]
    
def get_username():
    with open(os.path.join(os.path.dirname(__file__), 'google_secrets.json'), 'r') as f:
        data = json.load(f)
        return data["username"]
    
def request_token(username, scope, play_services = False):

    aas_token = get_aas_token()
    android_id = FcmReceiver().get_android_id()
    request_app = 'com.google.android.gms' if play_services else 'com.google.android.apps.adm'

    auth_response = gpsoauth.perform_oauth(
        username, aas_token, android_id,
        service='oauth2:https://www.googleapis.com/auth/' + scope,
        app=request_app,
        client_sig='38918a453d07199354f8b19af05ec6562ced5788')
    token = auth_response['Auth']

    return token

def get_adm_token(username):
    return request_token(username, "android_device_manager")

def get_spot_token(username):
    return request_token(username, "spot", True)