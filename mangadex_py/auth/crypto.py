import base64, binascii
from .auth_fs import deserialize_json


def create_json_sample(token, refresh) :
    sample = str({"token": token, "refresh": refresh})
    return sample

def base64_encrypt(json_sample) :
    bytes = json_sample.encode("utf-8")
    base64_encrypted = base64.b64encode(bytes)
    return base64_encrypted

def base64_decrypt(base64bytes) :
    base64_decrypted = base64.b64decode(base64bytes)
    return base64_decrypted

def hex_encrypt(base64_encrypted) :
    return binascii.hexlify(base64_encrypted)

def hex_decrypt(hexbytes) :
    return binascii.unhexlify(hexbytes)

def encrypt(token, refresh) :
    json_sample = create_json_sample(token, refresh)
    base64_encrypted = base64_encrypt(json_sample)
    hex_encrypted = hex_encrypt(base64_encrypted)
    return hex_encrypted

def decrypt(hex_encrypted) :
    base64_e = hex_decrypt(hex_encrypted)
    json_bytes = base64_decrypt(base64_e).decode("utf-8")
    json_data = deserialize_json(json_bytes)
    return json_data