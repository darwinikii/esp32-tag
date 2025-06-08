from google.ProtoDecoders import Common_pb2, DeviceUpdate_pb2
from google.ProtoDecoders.decoder import parse_device_list_protobuf, get_canonic_ids
from google.ProtoDecoders.DeviceUpdate_pb2 import DeviceRegistration
from google.util import generate_random_uuid
from google.NovaApi.nova_request import nova_request
from google.NovaApi.scopes import NOVA_LIST_DEVICS_API_SCOPE, NOVA_ACTION_API_SCOPE
from google.ProtoDecoders.decoder import parse_device_update_protobuf
from google.Auth.fcm_receiver import FcmReceiver
from google.Key.cloud_key_decryptor import decrypt_eik, decrypt_aes_gcm
from google.Crypto.foreign_tracker_cryptor import decrypt
from google.SpotApi.CreateBleDevice.config import mcu_fast_pair_model_id
from google.SpotApi.CreateBleDevice.util import flip_bits
from google.SpotApi.GetEidInfoForE2eeDevices.get_eid_info_request import get_eid_info
from google.SpotApi.GetEidInfoForE2eeDevices.get_owner_key import get_owner_key
import binascii, asyncio, hashlib

client_id = generate_random_uuid()

def create_action_request(canonic_device_id, gcm_registration_id, request_uuid = generate_random_uuid(), fmd_client_uuid = client_id):
    action_request = DeviceUpdate_pb2.ExecuteActionRequest()

    action_request.scope.type = DeviceUpdate_pb2.DeviceType.SPOT_DEVICE
    action_request.scope.device.canonicId.id = canonic_device_id

    action_request.requestMetadata.type = DeviceUpdate_pb2.DeviceType.SPOT_DEVICE
    action_request.requestMetadata.requestUuid = request_uuid

    action_request.requestMetadata.fmdClientUuid = fmd_client_uuid
    action_request.requestMetadata.gcmRegistrationId.id = gcm_registration_id
    action_request.requestMetadata.unknown = True

    return action_request

def create_device_list_request():
    wrapper = DeviceUpdate_pb2.DevicesListRequest()
    wrapper.deviceListRequestPayload.type = DeviceUpdate_pb2.DeviceType.SPOT_DEVICE
    wrapper.deviceListRequestPayload.id = generate_random_uuid()
    binary_payload = wrapper.SerializeToString()
    hex_payload = binascii.hexlify(binary_payload).decode('utf-8')
    return hex_payload

def create_location_request(canonic_device_id, fcm_registration_id, request_uuid):
    action_request = create_action_request(canonic_device_id, fcm_registration_id, request_uuid=request_uuid)
    # Random values, can be arbitrary
    action_request.action.locateTracker.lastHighTrafficEnablingTime.seconds = 1732120060
    action_request.action.locateTracker.contributorType = DeviceUpdate_pb2.SpotContributorType.FMDN_ALL_LOCATIONS
    # Convert to hex string
    hex_payload = serialize_action_request(action_request)

    return hex_payload

def request_google_device_list():
    hex_payload = create_device_list_request()
    result = nova_request(NOVA_LIST_DEVICS_API_SCOPE, hex_payload)
    device_list = parse_device_list_protobuf(result)
    device_list_parsed = get_canonic_ids(device_list)

    return device_list_parsed

def get_location_data_for_google_device(canonic_device_id):
    result = None
    request_uuid = generate_random_uuid()

    def handle_location_response(response):
        nonlocal result
        device_update = parse_device_update_protobuf(response)

        if device_update.fcmMetadata.requestUuid == request_uuid:
            result = parse_device_update_protobuf(response)
            #print_device_update_protobuf(response)

    fcm_token = FcmReceiver().register_for_location_updates(handle_location_response)

    hex_payload = create_location_request(canonic_device_id, fcm_token, request_uuid)
    nova_request(NOVA_ACTION_API_SCOPE, hex_payload)

    while result is None:
        asyncio.get_event_loop().run_until_complete(asyncio.sleep(0.1))

    return decrypt_location_response_locations(result)

def serialize_action_request(actionRequest):
    # Serialize to binary string
    binary_payload = actionRequest.SerializeToString()

    # Convert to hex string
    hex_payload = binascii.hexlify(binary_payload).decode('utf-8')

    return hex_payload

def decrypt_location_response_locations(device_update_protobuf):

    device_registration = device_update_protobuf.deviceMetadata.information.deviceRegistration

    identity_key = retrieve_identity_key(device_registration)
    locations_proto = device_update_protobuf.deviceMetadata.information.locationInformation.reports.recentLocationAndNetworkLocations
    is_mcu = is_mcu_tracker(device_registration)

    # At All Areas Reports or Own Reports
    recent_location = locations_proto.recentLocation
    recent_location_time = locations_proto.recentLocationTimestamp

    # High Traffic Reports
    network_locations = list(locations_proto.networkLocations)
    network_locations_time = list(locations_proto.networkLocationTimestamps)

    if locations_proto.HasField("recentLocation"):
        network_locations.append(recent_location)
        network_locations_time.append(recent_location_time)

    location_time_array = []
    for loc, time in zip(network_locations, network_locations_time):

        if loc.status == Common_pb2.Status.SEMANTIC:
            wrapped_location = {
                "decrypted_location": b'',
                "time": int(time.seconds),
                "accuracy": 0,
                "status": loc.status,
                "is_own_report": True,
                "name": loc.semanticLocation.locationName
            }
            location_time_array.append(wrapped_location)
        else:
            encrypted_location = loc.geoLocation.encryptedReport.encryptedLocation
            public_key_random = loc.geoLocation.encryptedReport.publicKeyRandom

            if public_key_random == b"":  # Own Report
                identity_key_hash = hashlib.sha256(identity_key).digest()
                decrypted_location = decrypt_aes_gcm(identity_key_hash, encrypted_location)
            else:
                time_offset = 0 if is_mcu else loc.geoLocation.deviceTimeOffset
                decrypted_location = decrypt(identity_key, encrypted_location, public_key_random, time_offset)

            proto_loc = DeviceUpdate_pb2.Location()
            proto_loc.ParseFromString(decrypted_location)

            latitude = proto_loc.latitude / 1e7
            longitude = proto_loc.longitude / 1e7
            altitude = proto_loc.altitude

            wrapped_location = {
                "location": (latitude, longitude, altitude),
                "time": int(time.seconds),
                "accuracy": loc.geoLocation.accuracy,
                "status": loc.status,
                "is_own_report": loc.geoLocation.encryptedReport.isOwnReport,
                "name": ""
            }
            location_time_array.append(wrapped_location)
    return location_time_array

# Indicates if the device is a custom microcontroller
def is_mcu_tracker(device_registration: DeviceRegistration) -> bool:
    return device_registration.fastPairModelId == mcu_fast_pair_model_id


def retrieve_identity_key(device_registration: DeviceRegistration) -> bytes:
    is_mcu = is_mcu_tracker(device_registration)
    encrypted_user_secrets = device_registration.encryptedUserSecrets

    encrypted_identity_key = flip_bits(
        encrypted_user_secrets.encryptedIdentityKey,
        is_mcu)
    owner_key = get_owner_key()

    try:
        identity_key = decrypt_eik(owner_key, encrypted_identity_key)
        return identity_key
    except Exception as e:
        print("Error decrypting identity key: ", e)
        return b''