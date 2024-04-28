import base64
from hashlib import scrypt
from os import urandom


def hash_password(password: str) -> str:
    salt = urandom(64)
    encoded_pass = base64.b64encode(
        scrypt(password.encode(), salt=salt, n=16, r=8, p=1)
    ).decode()
    return "$".join([base64.b64encode(salt).decode(), encoded_pass])


def verify_password(password: str, hash) -> bool:
    parts = hash.split("$")
    if len(parts) != 2:
        raise ValueError("Hash is not correctly formatted")
    salt = base64.b64decode(parts[0])
    decoded_hash = base64.b64decode(parts[1])
    hashed_password = scrypt(password.encode(), salt=salt, n=16, r=8, p=1)
    return hashed_password == decoded_hash
