from hashlib import sha256


def generate_secure_hash(hash_key: str, params: dict) -> str:
    values = "&".join(param[1] for param in sorted(params.items()))
    my_str = hash_key + "&" + values

    my_bytes = str.encode(my_str)
    my_sha256 = sha256(my_bytes)
    return my_sha256.hexdigest()
