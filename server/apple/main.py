import time
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, hmac
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from datetime import datetime, timezone, timedelta
from collections import OrderedDict
import requests
import json
import base64
from apple.anisette.main import generate_anisette_headers
from apple.Auth.main import getAuth
import os, uuid, locale, struct, math, hashlib

USER_ID = uuid.uuid4()
DEVICE_ID = uuid.uuid4()

def get_location_data_for_apple_device(device_id: str, device_private_key: str, days = 7) -> list:
    private_key = base64.b64decode(device_private_key)

    unixEpoch = int(time.time())
    startdate = unixEpoch - (60 * 60 * 24 * days)

    datetime.fromtimestamp(startdate)

    data = {
        "search": [
            {
                "startDate": 1,
                "ids": [device_id]
            }
        ]
    }

    anisette = generate_anisette_headers()
    anisette.update(generate_meta_headers(user_id=USER_ID, device_id=DEVICE_ID))

    with requests.post("https://gateway.icloud.com/acsnservice/fetch", auth=getAuth(), headers=anisette, json=data) as r:
        result = json.loads(r.content.decode())
        results = result['results']

        newResults = OrderedDict()

        for idx, entry in enumerate(results):
            entry['location'] = decrypt_report(entry, private_key)
            data = base64.b64decode(entry['payload'])
            timestamp = int.from_bytes(data[0:4], 'big') + 978307200
            if (timestamp > startdate):
                newResults[timestamp] = entry

        sorted_map = OrderedDict(sorted(newResults.items(), reverse=True))

        return sorted_map

def generate_meta_headers(serial="0", user_id=uuid.uuid4(), device_id=uuid.uuid4()):
    return {
        "X-Apple-I-Client-Time": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "X-Apple-I-TimeZone": "UTC",
        "loc": "en_US",
        "X-Apple-Locale": "en_US",
        "X-Apple-I-MD-RINFO": "50660608",  # either 17106176 or 50660608
        "X-Apple-I-MD-LU": base64.b64encode(str(user_id).upper().encode()).decode(),
        "X-Mme-Device-Id": str(device_id).upper(),
        "X-Apple-I-SRL-NO": serial,  # Serial number
    }

def decrypt_report(report: dict, key: bytes) -> dict:
    payload_data = base64.b64decode(report["payload"])

    # This part seems to handle a specific byte-length issue or format variation.
    # It removes the byte at index 4 if payload_data length is greater than 88.
    if len(payload_data) > 88:
        # Create a new bytearray and copy parts over, skipping index 4
        modified_data = bytearray(payload_data[:4] + payload_data[5:])
        payload_data = bytes(modified_data)

    ephemeral_key_bytes = payload_data[5:62]
    enc_data = payload_data[62:72]
    tag = payload_data[72:]

    _decode_time_and_confidence(payload_data, report)
    # Assuming 'key' is the private key in its raw byte form (e.g., 28 bytes for secp224r1)
    # Convert the raw private key bytes to an integer for EC.
    # The original Java code uses decodeBigIntWithSign(1, key), which implies
    # a positive BigInteger from the bytes.
    private_key_int = int.from_bytes(key, 'big')
    private_key = ec.derive_private_key(private_key_int, ec.SECP224R1(), default_backend())

    # The Java code decodes the point and then creates an ECPublicKey.
    # In `cryptography`, you typically load the public key directly from bytes
    # or derive it from the private key. Given `ephemeral_key_bytes` contains
    # the public key in a specific format, we'll try to load it.
    # The format (0x04 || X || Y) for uncompressed point.
    ephemeral_public_key = ec.EllipticCurvePublicKey.from_encoded_point(ec.SECP224R1(), ephemeral_key_bytes)

    shared_key_bytes = _ecdh(ephemeral_public_key, private_key)
    derived_key = _kdf(shared_key_bytes, ephemeral_key_bytes)

    decrypted_payload = _decrypt_payload(enc_data, derived_key, tag)
    location_report = _decode_payload(decrypted_payload, report)

    return location_report

def _decode_time_and_confidence(payload_data: bytearray, report: dict):
    # Python's int.from_bytes handles endianness
    seen_time_stamp = int.from_bytes(payload_data[0:4], 'big')
    timestamp = datetime(2001, 1, 1, 0, 0, 0, tzinfo=timezone.utc) + timedelta(seconds=seen_time_stamp)
    # Convert to local time if needed, similar to .toLocal() in Java
    timestamp = timestamp.astimezone() # Converts to local timezone

    confidence = payload_data[4]
    report["timestamp"] = timestamp.timestamp()
    report["confidence"] = confidence

def _ecdh(ephemeral_public_key: ec.EllipticCurvePublicKey, private_key: ec.EllipticCurvePrivateKey) -> bytes:
    # In cryptography, exchange returns the shared secret directly
    shared_key = private_key.exchange(ec.ECDH(), ephemeral_public_key)

    return shared_key

def _decode_payload(payload: bytes, report: dict) -> dict:
    latitude = int.from_bytes(payload[0:4], 'big')
    longitude = int.from_bytes(payload[4:8], 'big')
    accuracy = payload[8]
    status = payload[9]

    # Extract battery status if available
    battery_status = None
    if (status & 0x20) != 0 or status > 0:
        battery_status = status >> 6

    report["battery_status"] = battery_status

    latitude_dec = latitude / 10000000.0
    longitude_dec = longitude / 10000000.0

    return {
        "latitude": latitude_dec,
        "longitude": longitude_dec,
        "accuracy": accuracy,
    }

def _decrypt_payload(cipher_text: bytes, symmetric_key: bytes, tag: bytes) -> bytes:
    decryption_key = symmetric_key[0:16]
    iv = symmetric_key[16:] # IV is the rest of the symmetricKey after the 16-byte key

    decryptor = Cipher(
        algorithms.AES(decryption_key),
        modes.GCM(iv, tag),  # IV and tag for GCM
        backend=default_backend()
    ).decryptor()

    # Update with ciphertext
    plain_text = decryptor.update(cipher_text) + decryptor.finalize()
    return plain_text

def _kdf(secret: bytes, ephemeral_key: bytes) -> bytes:
    sha256 = hashes.Hash(hashes.SHA256(), backend=default_backend())
    sha256.update(secret)

    counter = 1
    counter_data_bytes = counter.to_bytes(4, 'big')
    sha256.update(counter_data_bytes)

    sha256.update(ephemeral_key)

    out = sha256.finalize()
    return out