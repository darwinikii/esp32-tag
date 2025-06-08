from google.main import request_google_device_list, get_location_data_for_google_device
from apple.main import get_location_data_for_apple_device
from util.local_devices import get_local_devices, get_local_device
import hashlib, json, os

def get_local_device_locations(device_hash):
    local_device = get_local_device(device_hash)
    local_device_locations = {}

    if local_device["google"]["enabled"] is True:
        google_device_list = request_google_device_list()
        google_device_canonicIds = [device[1] for device in google_device_list]

        if local_device["google"]["canonicId"] in google_device_canonicIds:
            locs = get_location_data_for_google_device(local_device['google']['canonicId'])
            for loc in locs:
                clean_loc = {
                    "type": "google",
                    "timestamp": loc['time'],
                    "datePublished": 0,
                    "location": {
                        "latitude": loc['location'][0],
                        "longitude": loc['location'][1],
                        "altitude": loc['location'][2],
                        "accuracy": loc['accuracy'],
                    },
                }
                loc_hash = hashlib.md5(bytearray(json.dumps(clean_loc), 'utf-8'))

                local_device_locations[loc_hash.hexdigest()] = clean_loc
    if local_device["apple"]["enabled"] is True:
        locs = get_location_data_for_apple_device(local_device['apple']['hashedAdvertisementKey'], local_device['apple']['privateKey'])
        for time in locs:
            loc = locs[time]

            clean_loc = {
                "type": "apple",
                "timestamp": time,
                "datePublished": loc['datePublished'],
                "location": {
                    "latitude": loc['location']['latitude'],
                    "longitude": loc['location']['longitude'],
                    "altitude": None,
                    "accuracy": loc['location']['accuracy'],
                },
            }
            loc_hash = hashlib.md5(bytearray(json.dumps(clean_loc), 'utf-8'))

            local_device_locations[loc_hash.hexdigest()] = clean_loc
    
    cached_locations = {}
    if not os.path.exists("devices/locationCache/" + device_hash):
        os.mkdir("devices/locationCache/" + device_hash)
    else:
        for file in os.listdir("devices/locationCache/" + device_hash):
            #read file
            with open("devices/locationCache/" + device_hash + "/" + file, "r") as f:
                cached_locations[file.split(".")[0]] = json.loads(f.read())

    for hash in local_device_locations.keys():
        location = local_device_locations[hash]
        with open("devices/locationCache/" + device_hash + "/" + str(hash) + ".json", "w") as f:
            f.write(json.dumps(location))

    return {**cached_locations, **local_device_locations}
    