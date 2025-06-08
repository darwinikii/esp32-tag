import os
import json
import hashlib

devices = {}
for file in os.listdir("devices"):
    if file.endswith(".json"):
        with open("devices/" + file) as f:
            data = json.load(f)
            hash = hashlib.md5(bytearray(f))
            devices[hash.hexdigest()] = data

def get_local_devices():
    return devices

def get_local_device(device_hash):
    return devices[device_hash]