from hashlib import sha256


def generate_secure_hash(hash_key: str, params: dict) -> str:

    values = "&".join(param[1] for param in sorted(params.items()) if param[1])
    my_str = hash_key + ("&" + values if values else "")

    my_bytes = str.encode(my_str)
    my_sha256 = sha256(my_bytes)
    return my_sha256.hexdigest()
